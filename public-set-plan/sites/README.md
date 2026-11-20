# DR Experiences landing pages

- **Live (Vercel project `dr-experiences`):** root directory `public-set-plan/sites`, production branch `claude/beautiful-gauss-q6z5r1`.
  `vercel.json` serves `/crew`, `/getaway`, `/celebrate` from `live/` (forms connected to the Supabase `quote` function).
- **Previews (claude.ai artifacts):** `crew.html`, `getaway.html`, `celebrate.html` at this folder's root (forms not connected).

## Rebuild after changing copy or photos
```
./build_live.sh        # builds live/ with the quote endpoint, then the preview copies
```
Commit and push: Vercel deploys the branch automatically.

## Prices
Live prices come from Supabase table `pricing_inputs`, loaded from `Villa_Getaway_Expenses_v10.xlsx`.
After editing the workbook: `python3 ../backend/scripts/import_pricing.py ../Villa_Getaway_Expenses_v10.xlsx > update.sql` and run it in Supabase.


