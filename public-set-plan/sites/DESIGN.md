# DR Experiences – Design System (three audience themes)

One brand and one content system, with three visual worlds. Each page shares the structure, the copy rules and the form. Colour, type and layout devices change per audience.

> This direction isn't based on real reference sites: UXKIN wasn't connected, and the owner's four Pinterest references couldn't be opened because the session network blocked them. Send screenshots to refine it.

## Shared rules (all three)
- **Spacing:** 8px scale (8, 16, 24, 32, 48, 72, 96). Sections use 72–96px of vertical padding. Content max width is 1180px, with a side gutter of at least 16px.
- **Body text:** 17px, line height 1.6, max 65 characters per line.
- **CTA:** one primary action per page ("Get my group's price" / "Plan my celebration"), repeated in the hero, the price section, the form, and a sticky bar on phones. There's no other navigation, following landing-page conversion practice.
- **Form:** the same fields everywhere. Consent boxes are unticked by default. Preview mode says that nothing was sent.
- **Images:** every placeholder shows its ID, type (Real / Created / Created now, swap for real) and subject. It never pretends to be the real villa or staff.
- **Copy:** follows the `copywriting` skill (no AI tells, claims must be supportable) and the guardrails in `DR_EXPERIENCES_LANDING_PAGES_PLAN.md` section 7.
- **Focus:** every interactive element shows a visible 3px focus ring. Motion respects `prefers-reduced-motion`.

## 1. The Crew – Dominican flag
**Feeling:** bold, sporty, a matchday poster. **Theme:** a single dark look (navy ground) with white bands.

| Token | Value | Role |
|---|---|---|
| `--navy` | #002D62 | Flag blue: panels, hero quadrants |
| `--navy-deep` | #001631 | Page background |
| `--red` | #CE1126 | Flag red: primary buttons, ticker, highlights (white text on red is 5.6:1) |
| `--white` | #FFFFFF | Flag white: the cross gutter, light bands, text on navy |
| `--paper` | #F3F6FB | Light band background (form, compare) |
| `--ink` | #0A1B33 | Text on light bands |
| `--soft` | #B9C8E0 | Secondary text on navy |

**Type:** *Anton* (condensed, uppercase display) + *Barlow* (body).
**Devices:**
- The **flag-cross hero**: a 2×2 grid split by white gutters, in flag order (blue | red / red | blue), with a round seal at the crossing.
- A red **ticker** band.
- The "**Lineup**" spec rows.
- "**Roster**" trading-card team cards.
- A "**Game plan**" timeline with times.
- **Ticket-stub** price cards.
- A "**Them vs. us**" scoreboard.

## 2. The Getaway – teal, sand and coral (kept from v1)
**Feeling:** soft, sunny, a magazine getaway spread. **Theme:** light and dark.

| Token | Light | Dark | Role |
|---|---|---|---|
| `--bg` | #F4F8F7 | #0B1514 | Page |
| `--surface` | #FFFFFF | #12201E | Cards, form |
| `--sand` | #F6EDE0 | #1A1712 | Story and moms bands |
| `--ink` | #0F1F1D | #E6F0EE | Text |
| `--muted` | #4A5F5B | #9BB1AC | Secondary text |
| `--sea` | #0E5C57 | #56C2B6 | Brand teal: links, chips |
| `--accent` | #C4503F | #F2958A | Coral: primary buttons, highlights |

**Type:** *DM Serif Display* (headlines, with italic for emphasis) + *Instrument Sans* (body) + *Caveat* (handwritten photo captions only).
**Devices:**
- **Arch-shaped** photo frames (villa windows).
- An overlapping circle photo and a floating note card in the hero.
- A curved path linking the three steps.
- A **swipeable team rail**.
- **Polaroid** day-in-the-life collage.
- A coral moms' band.

## 3. The Celebration – black and champagne gold
**Research:** black and gold is the most common palette for adult milestone parties (40th/50th), with blue-and-gold and jewel tones as other options ([source 1](https://www.thebash.com/articles/party-trends), [source 2](https://www.hallmark.ca/en/get-inspired/10-colourful-trendy-party-decorations-and-themes), [source 3](https://blog.1invites.com/birthday-invitation-design-trends/)). The sources are mostly party retailers and blogs, so treat this as a direction, not data.
**Feeling:** a black-tie invitation, a gala programme. **Theme:** a single dark look.

| Token | Value | Role |
|---|---|---|
| `--bg` | #0E0C09 | Page (warm black) |
| `--panel` | #17140E | Cards, form |
| `--gold` | #D9B76E | Champagne gold: buttons, rules, numerals (10.6:1 on bg) |
| `--ivory` | #F4ECDC | Text |
| `--muted` | #BFB29A | Secondary text |
| `--rose` / `--sky` | #E9A7B0 / #8FB0FF | Confetti accents only, never for text |

**Type:** *Bodoni Moda* (high-contrast display, with italic) + *Manrope* (body).
**Devices:**
- Giant **outlined gold numerals** (40 · 50 · 60) behind the hero.
- Restrained CSS **confetti**.
- **Place-card** occasion tiles.
- "**The menu**" of inclusions, with dotted leaders.
- "**Order of the evening**" programme timeline.
- Oval gold-framed team portraits.
- An **RSVP-card** form.
