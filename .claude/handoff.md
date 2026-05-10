# Handoff — 2026-05-10

## Summary
- Added a **👩‍⚕️ Disciplines** tab listing 20 mental health disciplines that work in inpatient settings
- Created `data_ai/mental_health_disciplines.csv` with columns: Discipline, Credentials, Education Required, Role in Inpatient Setting, Key Responsibilities, Setting Type, Licensure Body (CA)
- Disciplines tab includes search filter, setting type filter (Acute / Long-Term / Both), expandable cards with full detail, and a bar chart by setting type
- Updated **Recreational Therapist** setting type from "Long-Term" to "Acute & Long-Term"
- Restarted server to clear `@st.cache_data` after CSV edit so change was reflected
- Saved two checkpoints this session

## Current State
- **Branch:** main (clean, all committed and tagged as `checkpoint`)
- **Server:** running on port 8501
- **Key files:**
  - `app.py` — full app with 5 tabs: Hospital Cards, Full Table, Map, Disciplines, Charts
  - `data/hospital locations 22.csv` — 49 inpatient hospitals (source data, read-only)
  - `data_ai/mental_health_disciplines.csv` — 20 disciplines (editable)
  - `data_ai/hospital_coords.csv` — lat/lon for all 49 hospitals
- **App URL:** https://glowing-space-computing-machine-wv74r5qqvrvph9qwx-8501.app.github.dev

## Next Steps
- User may want to add more disciplines or edit existing entries
- Could add a "discipline profile" detail page or modal
- Could link disciplines to specific hospitals (e.g., which hospitals employ which disciplines)
- Could add a glossary or credential explanation section
- Could add outpatient programs as a separate tab using `data/hospital locations.csv`

## Key Decisions
- Disciplines data stored in `data_ai/mental_health_disciplines.csv` — easy to edit without touching `app.py`
- Used `st.expander()` for each discipline card to keep the tab scannable without overwhelming the user
- Setting Type values must be exactly: `"Acute"`, `"Long-Term"`, or `"Acute & Long-Term"` — the filter selectbox matches on these exact strings
- After editing the CSV, a server restart (not just a browser refresh) is required to clear `@st.cache_data`

## Watchouts
- **Cache behavior:** `@st.cache_data` caches CSV reads at server startup. Editing a CSV while the server is running will NOT reflect until the server is restarted — a browser hard-refresh alone is not enough
- **Setting Type filter:** The selectbox options are hardcoded as `["All", "Acute", "Long-Term", "Acute & Long-Term"]` — if a new setting type value is added to the CSV that doesn't match one of these exactly, it won't appear in the filter
- **SVG header:** Encoded as base64 `<img>` tag — do not switch back to inline `<svg>` with `<defs>`, Streamlit sanitizes gradient definitions
- **Map tiles:** Uses CartoDB Positron (free, no API key). Do not switch to `mapbox://` style URLs without adding a token
- **Server restart command:** `streamlit run app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true --server.enableCORS false --server.enableXsrfProtection false &`
