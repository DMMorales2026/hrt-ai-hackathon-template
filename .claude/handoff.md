# Handoff — 2026-05-10

## Summary
- Added **🏢 Outpatient Programs** tab using `data/hospital locations 11.csv` (49 programs)
  - Filters: search by keyword, county multiselect, population served multiselect
  - 4 summary metrics: programs found, counties, programs serving youth, programs with SUD services
  - Blue-bordered cards (distinct from inpatient orange) with address, phone, insurance, services, and website
  - Bar chart of programs by county
- Created `data_ai/outpatient_coords.csv` with lat/lon for all 49 outpatient programs (city-level precision)
- Added **🗺️ Outpatient Map** tab with interactive pydeck map
  - Blue circles (distinct from inpatient orange circles)
  - County filter, hover tooltips (program name, city, county, type, services, phone)
  - Reference table below the map
- Removed 🏥 icon from the wellness banner header
- Saved one checkpoint this session

## Current State
- **Branch:** main (3 commits ahead of origin, uncommitted changes remain)
- **Server:** running on port 8501
- **Modified/untracked files not yet committed:**
  - `app.py` (outpatient tab + outpatient map tab added, banner icon removed)
  - `data/hospital locations 11.csv` (untracked — new source file)
  - `data_ai/outpatient_coords.csv` (untracked — new coords file)
- **App tabs (in order):** Hospital Cards · Full Table · Map · Charts · Outpatient Programs · Outpatient Map · Disciplines
- **App URL:** https://glowing-space-computing-machine-wv74r5qqvrvph9qwx-8501.app.github.dev

## Next Steps
- Run `/checkpoint` to commit and tag the outpatient map work
- Could combine both maps (inpatient + outpatient) into a single unified map tab with color-coded layers
- Could add insurance filter to the outpatient tab (mirrors inpatient sidebar)
- Could add a "Services" tag breakdown chart to the outpatient tab
- Could add outpatient program detail panel (like the inpatient Full Table tab)

## Key Decisions
- Outpatient map uses **blue circles** (`[37, 99, 235]`) vs inpatient **orange circles** (`[192, 82, 42]`) for visual distinction
- Outpatient map dots use a **fixed radius of 8000m** (no bed-count scaling, since outpatient has no bed data)
- Outpatient coords stored in `data_ai/outpatient_coords.csv` and merged at load time in `load_outpatient()`
- Kept outpatient programs and outpatient map as two separate tabs rather than combining — gives user cleaner navigation between list and map views

## Watchouts
- **`data/hospital locations 11.csv` is untracked** — will be lost if the Codespace is reset without committing. Run `/checkpoint` soon.
- **`data_ai/outpatient_coords.csv` is untracked** — same risk as above.
- **Cache behavior:** `@st.cache_data` on `load_outpatient()` caches on server start. Any CSV edits require a server restart to take effect.
- **Map tiles:** Both maps use CartoDB Positron (`https://basemaps.cartocdn.com/gl/positron-gl-style/style.json`). Do not switch to `mapbox://` URLs without a token.
- **Tab order is hardcoded** in the `st.tabs()` call — adding/removing tabs requires updating both the tab list and the `with tab_X:` blocks in sync.
- **Server restart command:** `streamlit run app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true --server.enableCORS false --server.enableXsrfProtection false &`
