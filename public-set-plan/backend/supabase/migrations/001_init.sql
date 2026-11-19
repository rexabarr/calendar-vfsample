-- DR Experiences: pricing inputs (from Villa_Getaway_Expenses_v10.xlsx, Public Set tab) and leads.
-- Row Level Security is on with no public policies: only the `quote` edge function (service role) reads or writes.

create table if not exists public.pricing_inputs (
  key         text primary key,
  value       numeric not null,
  label       text not null,
  updated_at  timestamptz not null default now()
);

create table if not exists public.leads (
  id             uuid primary key default gen_random_uuid(),
  created_at     timestamptz not null default now(),
  page           text,
  first_name     text not null,
  last_name      text not null,
  email          text not null,
  phone          text not null,
  contact_method text,
  guests         text not null,
  occasion       text,
  arrival_date   date,
  nights         text,
  flexible       boolean default false,
  notes          text,
  heard          text,
  sms_consent    boolean default false,
  email_consent  boolean default false,
  quote_status   text,              -- quoted | custom
  bedrooms       int,
  quote_total    numeric,
  quote_per_person numeric,
  email_status   text,              -- sent | failed | skipped
  sales_status   text default 'new' -- new | contacted | quoted | deposit | lost
);

alter table public.pricing_inputs enable row level security;
alter table public.leads enable row level security;

create index if not exists leads_created_idx on public.leads (created_at desc);
create index if not exists leads_email_idx on public.leads (lower(email), created_at desc);

-- Seed: Public Set assumptions (per bedroom unless marked flat). Re-run scripts/import_pricing.py after editing the workbook.
insert into public.pricing_inputs (key, value, label) values
  ('villa_per_bedroom_night',        100,    'Villa ($/bedroom/night)'),
  ('chef_per_bedroom_dinner',        75,     'Chef, dinners only ($/bedroom/dinner night)'),
  ('housekeeper_per_bedroom_day',    60,     'Housekeeper, breakfast + lunch ($/bedroom/day)'),
  ('groceries_per_bedroom_night',    62.5,   'Groceries ($/bedroom/night)'),
  ('driver_per_bedroom_day',         225,    'Car + driver ($/bedroom/day)'),
  ('security_per_bedroom_night',     18.75,  'Security ($/bedroom/night)'),
  ('flat_welcome_kit',               65,     'Welcome kit (flat)'),
  ('flat_admin',                     150,    'Admin (flat)'),
  ('flat_marketing',                 100,    'Marketing (flat)'),
  ('flat_website',                   55,     'Website + maintenance (flat)'),
  ('flat_fuel',                      35,     'Fuel (flat)'),
  ('flat_insurance_taxes',           22,     'Insurance + taxes (flat)'),
  ('target_profit_per_guest_night',  350,    'Target profit per (guest + night) ($)'),
  ('card_rate',                      0.029,  'Card processing rate'),
  ('card_fixed_fee',                 0.30,   'Card fixed fee per transaction ($)'),
  ('max_auto_nights',                6,      'Longest stay priced automatically (longer = custom quote)'),
  ('max_auto_guests',                8,      'Largest group priced automatically')
on conflict (key) do update set value = excluded.value, label = excluded.label, updated_at = now();
