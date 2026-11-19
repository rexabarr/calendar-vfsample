"""Read the Public Set assumptions from the pricing workbook and print SQL that updates Supabase.
Usage:  python3 import_pricing.py Villa_Getaway_Expenses_v10.xlsx > update.sql
Then paste update.sql into Supabase > SQL editor (or ask Claude to run it).
Also checks the instant-quote formula against every LIST PRICE in the workbook."""
import math, sys, openpyxl

LABELS = {  # workbook label (start of text) -> pricing_inputs key
    "Villa ($/bedroom/night": "villa_per_bedroom_night",
    "Chef – dinners only": "chef_per_bedroom_dinner",
    "Housekeeper – breakfast + lunch": "housekeeper_per_bedroom_day",
    "Groceries ($/bedroom/night)": "groceries_per_bedroom_night",
    "Car + driver ($/bedroom/day)": "driver_per_bedroom_day",
    "Security ($/bedroom/night)": "security_per_bedroom_night",
    "Welcome kit (flat)": "flat_welcome_kit",
    "Admin (flat)": "flat_admin",
    "Marketing (flat)": "flat_marketing",
    "Website + maintenance (flat)": "flat_website",
    "Fuel (flat)": "flat_fuel",
    "Insurance + taxes (flat)": "flat_insurance_taxes",
    "Target profit per (guest + night)": "target_profit_per_guest_night",
}

def read_inputs(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    vals = {}
    for r in wb["Public Set"].iter_rows(min_row=1, max_row=25, values_only=True):
        if r[0] is None: continue
        for prefix, key in LABELS.items():
            if str(r[0]).startswith(prefix) and isinstance(r[1], (int, float)):
                vals[key] = r[1]
    ie = wb["Itemized Expenses"]
    for r in ie.iter_rows(min_row=1, max_row=10, values_only=True):
        if r[0] == "Card processing rate": vals["card_rate"] = r[1]
        if r[0] and str(r[0]).startswith("Card fixed fee"): vals["card_fixed_fee"] = r[1]
    missing = set(LABELS.values()) | {"card_rate", "card_fixed_fee"}
    missing -= set(vals)
    if missing: sys.exit(f"Missing in workbook: {sorted(missing)}")
    return vals, wb

def price(i, guests, nights):  # mirrors supabase/functions/quote/index.ts
    b = math.ceil(guests / 2)
    costs = (b * nights * (i["villa_per_bedroom_night"] + i["groceries_per_bedroom_night"] + i["driver_per_bedroom_day"] + i["security_per_bedroom_night"])
             + b * (nights - 1) * (i["chef_per_bedroom_dinner"] + i["housekeeper_per_bedroom_day"])
             + sum(i[k] for k in i if k.startswith("flat_")))
    return math.ceil((costs + i["card_fixed_fee"] + (guests + nights) * i["target_profit_per_guest_night"]) / (1 - i["card_rate"]) / 10) * 10

def check(i, wb):
    ws = wb["Public Set"]; bedrooms = guests = None; bad = 0; n = 0
    for r in ws.iter_rows(values_only=True):
        if r[0] == "Bedrooms": bedrooms = r[1]
        if r[0] and str(r[0]).startswith("Guests"): guests = r[1]
        if r[0] == "LIST PRICE":
            for nights, wbp in zip((3, 4, 5, 6), r[1:5]):
                n += 1; ours = price(i, guests, nights)
                if abs(ours - wbp) > 0.01: bad += 1; print(f"-- MISMATCH {bedrooms}BR {guests}g {nights}n: workbook {wbp} vs formula {ours}", file=sys.stderr)
    print(f"-- formula check: {n - bad}/{n} workbook prices match", file=sys.stderr)
    return bad == 0

if __name__ == "__main__":
    vals, wb = read_inputs(sys.argv[1])
    ok = check(vals, wb)
    print("-- generated from", sys.argv[1])
    for k, v in vals.items():
        print(f"update public.pricing_inputs set value = {v}, updated_at = now() where key = '{k}';")
    sys.exit(0 if ok else 1)
