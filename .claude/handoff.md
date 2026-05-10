# Handoff — 2026-05-10

## Summary
- Added **🏠 Home** tab as the first tab with welcome message, 5 quick stats, color-coded "What's Inside" feature cards, and a quick-reference "How to Get Started" table
- Added **📊 Outpatient Charts** tab then removed it at user request
- Removed multiple emoji icons from section headers across tabs (Home, Outpatient Programs, Outpatient Map, Disciplines)
- Renamed tabs:
  - "Hospital Cards" → **Inpatient Hospital Cards**
  - "Full Table" → **Inpatient Full List**
  - "Map" → **Inpatient Map**
  - "Charts" → **Inpatient Charts**
- Updated banner title to **"California's Mental Health Programs Directory"**
- Removed "Hospitals by Accreditation" chart from Inpatient Charts tab; cleaned up layout from 2-column to single column
- Removed "Disciplines by Setting Type" chart from Disciplines tab
- Removed 🛏️ icon from "Bed Capacity by County" chart heading

## Current State
- **Branch:** main (4 commits ahead of origin, app.py has uncommitted changes)
- **Server:** running on port 8501
- **Tab order (8 tabs):** Home · Inpatient Hospital Cards · Inpatient Full List · Inpatient Map · Inpatient Charts · Outpatient Programs · Outpatient Map · Disciplines
- **App URL:** https://glowing-space-computing-machine-wv74r5qqvrvph9qwx-8501.app.github.dev

## Next Steps
- Run `/checkpoint` to commit current uncommitted changes to app.py
- Could update the Home tab "What's Inside" cards to reflect the renamed tabs
- Could update page config title (`st.set_page_config`) to match new banner title
- Could add an outpatient charts tab back if needed in the future
- Could add filter for insurance on the Outpatient Programs tab

## Key Decisions
- All tab renames are in the single `st.tabs([...])` call — both the list entry and the `with tab_X:` block must stay in sync
- Emoji icons removed from section headers throughout for a cleaner, more professional look
- Home tab loads all three datasets (`load_data`, `load_outpatient`, `load_disciplines`) to compute live stats — no additional caching needed

## Watchouts
- **app.py has uncommitted changes** — run `/checkpoint` before ending the session or the work will be lost on Codespace reset
- **Tab variable names** are positional — if tabs are reordered or added/removed, every `with tab_X:` block below must be updated to match the new order
- **Home tab stats** pull from the full unfiltered datasets, not the sidebar-filtered data — this is intentional so counts always reflect the full directory
- **Server restart command:** `streamlit run app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true --server.enableCORS false --server.enableXsrfProtection false &`
