// DR Experiences instant quote.
// POST JSON from the landing page form -> validates, prices the trip with the workbook formula,
// saves the lead, emails the guest their estimate and alerts the sales team.
// Secrets (set in Supabase > Edge Functions > Secrets): RESEND_API_KEY, FROM_EMAIL, SALES_EMAIL, ALLOWED_ORIGINS (comma list, optional).
import { createClient } from "npm:@supabase/supabase-js@2";

const HOURS = "between 10am and 4pm ET";
const supabase = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);

function cors(origin: string | null) {
  const allowed = (Deno.env.get("ALLOWED_ORIGINS") ?? "*").split(",").map((s) => s.trim());
  const ok = allowed.includes("*") || (origin && allowed.includes(origin));
  return {
    "Access-Control-Allow-Origin": ok ? (origin ?? "*") : allowed[0],
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "content-type",
    "Vary": "Origin",
  };
}

type Inputs = Record<string, number>;

// Same formula as the Public Set tab:
// nightly lines = rate x bedrooms x nights; chef dinners and housekeeper days = nights - 1;
// price = ROUNDUP((costs + fixed fee + (guests + nights) x profit rate) / (1 - card rate), -1)
export function priceTrip(i: Inputs, guests: number, nights: number) {
  const bedrooms = Math.ceil(guests / 2);
  const nightly = (rate: number, count: number) => rate * bedrooms * count;
  const costs =
    nightly(i.villa_per_bedroom_night, nights) +
    nightly(i.chef_per_bedroom_dinner, nights - 1) +
    nightly(i.housekeeper_per_bedroom_day, nights - 1) +
    nightly(i.groceries_per_bedroom_night, nights) +
    nightly(i.driver_per_bedroom_day, nights) +
    nightly(i.security_per_bedroom_night, nights) +
    i.flat_welcome_kit + i.flat_admin + i.flat_marketing + i.flat_website + i.flat_fuel + i.flat_insurance_taxes;
  const target = (guests + nights) * i.target_profit_per_guest_night;
  const total = Math.ceil((costs + i.card_fixed_fee + target) / (1 - i.card_rate) / 10) * 10;
  return { bedrooms, total, perPerson: Math.round((total / guests) * 100) / 100 };
}

const money = (n: number) => "$" + n.toLocaleString("en-US", { minimumFractionDigits: 0, maximumFractionDigits: 2 });
const esc = (s: string) => s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]!));

async function sendEmail(to: string, subject: string, html: string) {
  const key = Deno.env.get("RESEND_API_KEY");
  if (!key) return "skipped";
  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
    body: JSON.stringify({ from: Deno.env.get("FROM_EMAIL") ?? "DR Experiences <onboarding@resend.dev>", to: [to], subject, html }),
  });
  return res.ok ? "sent" : "failed";
}

function guestEmail(first: string, q: { status: string; guests: number; nights: number; total?: number; perPerson?: number; bedrooms?: number; arrival?: string }) {
  const intro = q.status === "quoted"
    ? `<p>Here's your estimate for <b>${q.guests} guests, ${q.nights} nights</b> in a private ${q.bedrooms}-bedroom villa${q.arrival ? `, arriving ${esc(q.arrival)}` : ""}:</p>
       <p style="font-size:28px;margin:8px 0"><b>${money(q.perPerson!)} per person</b></p><p>${money(q.total!)} total for the group.</p>`
    : `<p>Thanks for telling us about your trip. For stays of 7 nights or more, or groups larger than 8, our team puts together a custom quote. We'll reach out ${HOURS}.</p>`;
  return `<div style="font-family:Arial,sans-serif;font-size:16px;line-height:1.6;color:#10201f;max-width:560px">
  <p>Hi ${esc(first)},</p>${intro}
  <p><b>Included:</b> private villa with a private pool minutes from the beach, breakfast and lunch every full day, private-chef dinners every night but one, private car service with security for scheduled outings, your personal concierge plus a 24/7 AI concierge assistant, early check-in from 12pm, and a welcome kit.</p>
  <p><b>Not included:</b> flights, excursions (booked at least 15% below resort prices), drinks and meals out, gratuities and travel insurance.</p>
  <p><b>What happens next:</b> a real person on our team will confirm villa availability for your dates and reach out ${HOURS}. No payment is needed until you're ready. A 50% deposit holds your dates and the balance is due 30 days before arrival.</p>
  <p style="color:#4a5f5b;font-size:13px">This is an estimate based on your group size and stay length. Final price is confirmed in writing once availability is checked. Excursions are priced separately.</p>
  <p>DR Experiences</p></div>`;
}

Deno.serve(async (req) => {
  const headers = { ...cors(req.headers.get("origin")), "Content-Type": "application/json" };
  if (req.method === "OPTIONS") return new Response(null, { headers });
  if (req.method !== "POST") return new Response(JSON.stringify({ error: "method" }), { status: 405, headers });

  let b: Record<string, unknown>;
  try { b = await req.json(); } catch { return new Response(JSON.stringify({ error: "bad_json" }), { status: 400, headers }); }
  if (b.website) return new Response(JSON.stringify({ status: "ok" }), { headers }); // honeypot

  const str = (k: string, max = 200) => (typeof b[k] === "string" ? (b[k] as string).trim().slice(0, max) : "");
  const first = str("first", 80), last = str("last", 80), email = str("email", 160).toLowerCase(), phone = str("phone", 40);
  const guestsRaw = str("size", 10), nightsRaw = str("nights", 10), arrival = str("arrival", 10);
  if (!first || !last || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email) || phone.length < 7 || !guestsRaw) {
    return new Response(JSON.stringify({ error: "missing_fields" }), { status: 422, headers });
  }

  // basic abuse limit: 5 submissions per email per hour
  const since = new Date(Date.now() - 3600_000).toISOString();
  const { count } = await supabase.from("leads").select("id", { count: "exact", head: true }).eq("email", email).gte("created_at", since);
  if ((count ?? 0) >= 5) return new Response(JSON.stringify({ error: "rate_limited" }), { status: 429, headers });

  const { data: rows, error } = await supabase.from("pricing_inputs").select("key,value");
  if (error || !rows) return new Response(JSON.stringify({ error: "pricing_unavailable" }), { status: 500, headers });
  const inputs: Inputs = Object.fromEntries(rows.map((r) => [r.key, Number(r.value)]));

  const guests = parseInt(guestsRaw, 10), nights = parseInt(nightsRaw, 10);
  const auto = Number.isFinite(guests) && guests >= 2 && guests <= inputs.max_auto_guests && !/\+/.test(guestsRaw)
            && Number.isFinite(nights) && nights >= 3 && nights <= inputs.max_auto_nights && !/\+/.test(nightsRaw);
  const q = auto ? priceTrip(inputs, guests, nights) : null;
  const status = q ? "quoted" : "custom";

  const subject = q ? `Your DR Experiences estimate: ${money(q.perPerson)} per person` : "Your DR Experiences trip: custom quote on the way";
  const emailStatus = await sendEmail(email, subject, guestEmail(first, { status, guests, nights, total: q?.total, perPerson: q?.perPerson, bedrooms: q?.bedrooms, arrival }));

  const sales = Deno.env.get("SALES_EMAIL");
  if (sales) {
    await sendEmail(sales, `New ${str("page", 20) || "site"} lead: ${first} ${last}, ${guestsRaw} guests, ${nightsRaw || "?"} nights`,
      `<pre style="font-family:monospace">${esc(JSON.stringify({ ...b, website: undefined, quote: q ?? "custom" }, null, 2))}</pre>`);
  }

  await supabase.from("leads").insert({
    page: str("page", 20), first_name: first, last_name: last, email, phone, contact_method: str("method", 20),
    guests: guestsRaw, occasion: str("occasion", 60), arrival_date: /^\d{4}-\d{2}-\d{2}$/.test(arrival) ? arrival : null,
    nights: nightsRaw, flexible: !!b.flexible, notes: str("notes", 2000), heard: str("heard", 40),
    sms_consent: !!b.sms, email_consent: !!b.news, quote_status: status, bedrooms: q?.bedrooms ?? null,
    quote_total: q?.total ?? null, quote_per_person: q?.perPerson ?? null, email_status: emailStatus,
  });

  return new Response(JSON.stringify({ status, guests, nights, ...(q ?? {}), email_status: emailStatus }), { headers });
});
