# Handoff — 2026-05-10

## Summary
- Built a Streamlit app (`app.py`) listing California inpatient mental health hospitals
- Data source: `data/hospital locations 22.csv` (49 hospitals, no Organization Type column)
- Created `data_ai/hospital_coords.csv` with lat/lon for all 49 hospitals (manually geocoded by city)
- Added interactive pydeck map using CartoDB Positron tiles (no API key required)
- Added sidebar filters: search, county, population served, insurance accepted, bed count slider
- Added 5 summary metrics: hospitals found, total beds, counties, Joint Commission count, CDPH licensed count
- Added 3 tabs: Hospital Cards, Full Table (with detail panel), Map, Charts
- Styled cards: white background, slate gray left border, drop shadow
- Set soft blue app background (#dbeafe) and slightly deeper blue sidebar (#bfdbfe)
- Added holistic wellness SVG header (purple-to-orange sunrise, lotus flowers, stars, light rays, water ripples)
- Fixed SVG rendering issue by encoding as base64 `<img>` tag to bypass Streamlit's HTML sanitizer

## Current State
- **Branch:** main (up to date with origin, changes not committed)
- **Server:** running on port 8501
- **Modified files:** `app.py`, `requirements.txt`
- **Untracked files:** `data/hospital locations 22.csv`, `data_ai/behavioral_health_programs.csv`, `data_ai/hospital_coords.csv`
- **App URL:** https://glowing-space-computing-machine-wv74r5qqvrvph9qwx-8501.app.github.dev

## Next Steps
- Commit all changes to git
- User may want to continue customizing the design (fonts, card layout, colors)
- Could add a 2-3 column card grid layout instead of single-column
- Could add a "Contact / Refer" button on each card
- Could add export to CSV or PDF functionality
- Could integrate outpatient data (`data/hospital locations.csv`) as a toggle

## Key Decisions
- Used `data/hospital locations 22.csv` (not `hospital locations 2.csv`) — new file dropped "Organization Type" column; replaced that metric with "CDPH Licensed" count
- Used CartoDB Positron map style (`https://basemaps.cartocdn.com/gl/positron-gl-style/style.json`) instead of Mapbox — no API key needed
- Hospital coordinates stored in `data_ai/hospital_coords.csv` and merged at load time — city-level precision
- SVG header encoded as base64 `<img>` tag — inline SVGs with `<defs>` gradients were being sanitized by Streamlit and not rendering
- Replaced "Private Hospitals" metric with "CDPH Licensed" since Organization Type column was removed

## Watchouts
- **SVG in Streamlit:** Never use raw inline `<svg>` with `<defs>` gradients in `st.markdown()` — Streamlit sanitizes them. Always encode as base64 and embed as `<img src="data:image/svg+xml;base64,..."/>`
- **Mapbox tiles:** `mapbox://styles/...` URLs require a token and will show a blank map. Always use CartoDB or another open tile provider
- **`use_container_width` deprecation:** Streamlit now prefers `width='stretch'` — already updated in the table views
- **Streamlit server:** The server stops when the Codespace idles. Restart with: `streamlit run app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true --server.enableCORS false --server.enableXsrfProtection false &`
- **data/ folder:** Never write to or modify files in `data/` — it is read-only per project rules
