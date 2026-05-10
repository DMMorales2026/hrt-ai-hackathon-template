import streamlit as st
import pandas as pd
import pydeck as pdk
import base64

st.set_page_config(
    page_title="California Inpatient Mental Health Hospitals",
    layout="wide",
    page_icon="🏥"
)

st.markdown("""
<style>
    /* App background */
    .stApp { background-color: #dbeafe; }

    /* Sidebar background */
    [data-testid="stSidebar"] { background-color: #bfdbfe; }

    /* Main content block */
    [data-testid="stMainBlockContainer"] { background-color: transparent; }

    .card {
        background: #ffffff;
        border-left: 6px solid #94a3b8;
        border-radius: 10px;
        padding: 18px 22px;
        margin-bottom: 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.10);
    }
    .card h4 { margin: 0 0 8px 0; font-size: 17px; color: #1e293b; }
    .badge {
        display: inline-block;
        padding: 3px 11px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 700;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    .badge-org   { background: #fde8d8; color: #8b3a10; }
    .badge-type  { background: #eaf4ec; color: #1a6b30; }
    .badge-pop   { background: #f0eafd; color: #4a1a8a; }
    .card-meta   { font-size: 13px; color: #444; line-height: 2.1; margin-top: 8px; }
    .card-meta strong { color: #111; }
    .beds-pill {
        background: #c0522a;
        color: white;
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 13px;
        font-weight: 700;
        float: right;
    }
</style>
""", unsafe_allow_html=True)

# ── Load Data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/hospital locations 22.csv")
    df.columns = df.columns.str.strip()
    df["County"] = df["County"].str.strip()
    df["City"]   = df["City"].str.strip()
    df["Bed Count"] = pd.to_numeric(df["Bed Count"], errors="coerce")
    coords = pd.read_csv("data_ai/hospital_coords.csv")
    df = df.merge(coords, on="Hospital", how="left")
    return df

df = load_data()

# ── Header ─────────────────────────────────────────────────────────────────────
_svg = """
<svg viewBox="0 0 1200 200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#1a0533"/>
      <stop offset="55%"  stop-color="#6b21a8"/>
      <stop offset="100%" stop-color="#ea580c"/>
    </linearGradient>
    <radialGradient id="glow" cx="50%" cy="100%" r="70%">
      <stop offset="0%"   stop-color="#fbbf24" stop-opacity="0.7"/>
      <stop offset="60%"  stop-color="#a855f7" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#1a0533" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="1200" height="200" fill="url(#bg)"/>
  <rect width="1200" height="200" fill="url(#glow)"/>
  <g stroke="#fef08a" stroke-width="1" opacity="0.12">
    <line x1="600" y1="200" x2="0"    y2="0"/>
    <line x1="600" y1="200" x2="150"  y2="0"/>
    <line x1="600" y1="200" x2="300"  y2="0"/>
    <line x1="600" y1="200" x2="450"  y2="0"/>
    <line x1="600" y1="200" x2="600"  y2="0"/>
    <line x1="600" y1="200" x2="750"  y2="0"/>
    <line x1="600" y1="200" x2="900"  y2="0"/>
    <line x1="600" y1="200" x2="1050" y2="0"/>
    <line x1="600" y1="200" x2="1200" y2="0"/>
  </g>
  <circle cx="80"   cy="25" r="1.5" fill="white" opacity="0.8"/>
  <circle cx="190"  cy="45" r="2"   fill="white" opacity="0.7"/>
  <circle cx="310"  cy="20" r="1"   fill="white" opacity="0.9"/>
  <circle cx="420"  cy="38" r="1.5" fill="white" opacity="0.6"/>
  <circle cx="150"  cy="65" r="1"   fill="white" opacity="0.7"/>
  <circle cx="260"  cy="55" r="1"   fill="white" opacity="0.8"/>
  <circle cx="520"  cy="28" r="1.5" fill="white" opacity="0.6"/>
  <circle cx="680"  cy="18" r="1"   fill="white" opacity="0.7"/>
  <circle cx="780"  cy="22" r="1.5" fill="white" opacity="0.8"/>
  <circle cx="890"  cy="42" r="2"   fill="white" opacity="0.7"/>
  <circle cx="1010" cy="18" r="1"   fill="white" opacity="0.9"/>
  <circle cx="1120" cy="35" r="1.5" fill="white" opacity="0.6"/>
  <circle cx="950"  cy="62" r="1"   fill="white" opacity="0.7"/>
  <ellipse cx="600" cy="198" rx="570" ry="5"   fill="none" stroke="#fbbf24" stroke-width="0.8" opacity="0.3"/>
  <ellipse cx="600" cy="194" rx="430" ry="4"   fill="none" stroke="#fbbf24" stroke-width="0.8" opacity="0.35"/>
  <ellipse cx="600" cy="190" rx="300" ry="3"   fill="none" stroke="#fef08a" stroke-width="0.8" opacity="0.4"/>
  <g transform="translate(600,178)">
    <path d="M0,0 Q-20,-18 0,-42 Q20,-18 0,0"  fill="#f5d0fe" opacity="0.92"/>
    <path d="M0,0 Q-20,-18 0,-42 Q20,-18 0,0"  fill="#e879f9" opacity="0.85" transform="rotate(45)"/>
    <path d="M0,0 Q-20,-18 0,-42 Q20,-18 0,0"  fill="#d946ef" opacity="0.78" transform="rotate(90)"/>
    <path d="M0,0 Q-20,-18 0,-42 Q20,-18 0,0"  fill="#e879f9" opacity="0.82" transform="rotate(135)"/>
    <path d="M0,0 Q-20,-18 0,-42 Q20,-18 0,0"  fill="#f5d0fe" opacity="0.70" transform="rotate(180)"/>
    <path d="M0,0 Q-20,-18 0,-42 Q20,-18 0,0"  fill="#e879f9" opacity="0.72" transform="rotate(225)"/>
    <path d="M0,0 Q-20,-18 0,-42 Q20,-18 0,0"  fill="#d946ef" opacity="0.68" transform="rotate(270)"/>
    <path d="M0,0 Q-20,-18 0,-42 Q20,-18 0,0"  fill="#e879f9" opacity="0.72" transform="rotate(315)"/>
    <circle r="11" fill="#fde68a" opacity="0.95"/>
    <circle r="7"  fill="#f59e0b"/>
    <circle r="3"  fill="#fef9c3"/>
  </g>
  <g transform="translate(280,193)">
    <path d="M0,0 Q-12,-10 0,-24 Q12,-10 0,0" fill="#f5d0fe" opacity="0.75"/>
    <path d="M0,0 Q-12,-10 0,-24 Q12,-10 0,0" fill="#e879f9" opacity="0.70" transform="rotate(60)"/>
    <path d="M0,0 Q-12,-10 0,-24 Q12,-10 0,0" fill="#d946ef" opacity="0.65" transform="rotate(120)"/>
    <path d="M0,0 Q-12,-10 0,-24 Q12,-10 0,0" fill="#e879f9" opacity="0.65" transform="rotate(180)"/>
    <path d="M0,0 Q-12,-10 0,-24 Q12,-10 0,0" fill="#d946ef" opacity="0.60" transform="rotate(240)"/>
    <path d="M0,0 Q-12,-10 0,-24 Q12,-10 0,0" fill="#e879f9" opacity="0.60" transform="rotate(300)"/>
    <circle r="7" fill="#fde68a" opacity="0.90"/>
    <circle r="4" fill="#f59e0b"/>
  </g>
  <g transform="translate(920,193)">
    <path d="M0,0 Q-12,-10 0,-24 Q12,-10 0,0" fill="#f5d0fe" opacity="0.75"/>
    <path d="M0,0 Q-12,-10 0,-24 Q12,-10 0,0" fill="#e879f9" opacity="0.70" transform="rotate(60)"/>
    <path d="M0,0 Q-12,-10 0,-24 Q12,-10 0,0" fill="#d946ef" opacity="0.65" transform="rotate(120)"/>
    <path d="M0,0 Q-12,-10 0,-24 Q12,-10 0,0" fill="#e879f9" opacity="0.65" transform="rotate(180)"/>
    <path d="M0,0 Q-12,-10 0,-24 Q12,-10 0,0" fill="#d946ef" opacity="0.60" transform="rotate(240)"/>
    <path d="M0,0 Q-12,-10 0,-24 Q12,-10 0,0" fill="#e879f9" opacity="0.60" transform="rotate(300)"/>
    <circle r="7" fill="#fde68a" opacity="0.90"/>
    <circle r="4" fill="#f59e0b"/>
  </g>
  <circle cx="450" cy="168" r="2.5" fill="#f5d0fe" opacity="0.55"/>
  <circle cx="380" cy="152" r="1.5" fill="#fde68a" opacity="0.50"/>
  <circle cx="750" cy="163" r="2"   fill="#f5d0fe" opacity="0.55"/>
  <circle cx="820" cy="150" r="1.5" fill="#fde68a" opacity="0.50"/>
</svg>
"""
_b64 = base64.b64encode(_svg.encode()).decode()

st.markdown(f"""
<div style="position:relative; width:100%; border-radius:14px; overflow:hidden; margin-bottom:24px;">
  <img src="data:image/svg+xml;base64,{_b64}"
       style="display:block; width:100%; height:auto;"/>
  <div style="position:absolute; top:0; left:0; width:100%; height:100%;
              display:flex; flex-direction:column; justify-content:center;
              align-items:center; text-align:center; padding:16px;">
    <h1 style="color:white; font-size:2rem; font-weight:800; margin:0;
               text-shadow: 0 2px 10px rgba(0,0,0,0.7);">
      🏥 California Inpatient Mental Health Hospitals
    </h1>
    <p style="color:#fde68a; font-size:1rem; margin:8px 0 0 0;
              text-shadow: 0 1px 6px rgba(0,0,0,0.6);">
      Directory of inpatient psychiatric hospitals across California —
      state, county, academic, and private facilities
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar Filters ────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🔍 Filter Hospitals")

    search = st.text_input("Search by name, city, or keyword",
                           placeholder="e.g. UCLA, Sacramento, Forensic…")

    all_counties = sorted(df["County"].dropna().unique())
    counties = st.multiselect("County", options=all_counties,
                              default=[], placeholder="All counties")

    all_pop = sorted({p.strip()
                      for ps in df["Population Served"].dropna()
                      for p in ps.split(";")})
    pop_filter = st.multiselect("Population Served", options=all_pop,
                                default=[], placeholder="All populations")

    all_ins = sorted({i.strip()
                      for ins in df["Insurance Accepted"].dropna()
                      for i in ins.split(";")})
    ins_filter = st.multiselect("Insurance Accepted", options=all_ins,
                                default=[], placeholder="All insurers")

    bed_min, bed_max = int(df["Bed Count"].min()), int(df["Bed Count"].max())
    bed_range = st.slider("Bed Count Range", min_value=bed_min,
                          max_value=bed_max, value=(bed_min, bed_max))

    st.markdown("---")
    st.caption(f"Total hospitals in dataset: **{len(df)}**")

# ── Apply Filters ──────────────────────────────────────────────────────────────
filtered = df.copy()

if search:
    kw = search.lower()
    filtered = filtered[
        filtered["Hospital"].str.lower().str.contains(kw, na=False)
        | filtered["City"].str.lower().str.contains(kw, na=False)
        | filtered["Program Type"].str.lower().str.contains(kw, na=False)
    ]

if counties:
    filtered = filtered[filtered["County"].isin(counties)]

if pop_filter:
    filtered = filtered[
        filtered["Population Served"].apply(
            lambda x: any(p in str(x) for p in pop_filter)
        )
    ]

if ins_filter:
    filtered = filtered[
        filtered["Insurance Accepted"].apply(
            lambda x: any(i in str(x) for i in ins_filter)
        )
    ]

filtered = filtered[
    filtered["Bed Count"].between(bed_range[0], bed_range[1], inclusive="both")
]

# ── Summary Metrics ────────────────────────────────────────────────────────────
total_h  = len(filtered)
total_b  = int(filtered["Bed Count"].sum())
cnty_n   = filtered["County"].nunique()
jc_count  = filtered["Accreditation"].str.contains("Joint Commission", na=False).sum()
cdph_count = filtered["Accreditation"].str.contains("CDPH", na=False).sum()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Hospitals Found",     total_h)
c2.metric("🛏️ Total Beds",       total_b)
c3.metric("📍 Counties",         cnty_n)
c4.metric("✅ Joint Commission",  jc_count)
c5.metric("🏛️ CDPH Licensed",    cdph_count)

st.markdown("---")

if total_h == 0:
    st.warning("No hospitals match your filters. Try broadening your search.")
    st.stop()

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab_cards, tab_table, tab_map, tab_charts = st.tabs(["🗂 Hospital Cards", "📋 Full Table", "🗺️ Map", "📊 Charts"])

# ── CARDS ──────────────────────────────────────────────────────────────────────
with tab_cards:
    st.markdown(f"**{total_h} hospital{'s' if total_h != 1 else ''} found**")

    for _, row in filtered.iterrows():
        web_html = (f'<a href="{row["Website"]}" target="_blank">{row["Website"]}</a>'
                    if pd.notna(row["Website"]) else "—")

        st.markdown(f"""
        <div class="card">
            <div class="beds-pill">🛏️ {int(row['Bed Count'])} Beds</div>
            <h4>{row['Hospital']}</h4>
            <span class="badge badge-type">{row['Program Type']}</span>
            <span class="badge badge-pop">{row['Population Served']}</span>
            <div class="card-meta">
                <span>📍 <strong>{row['Address']}</strong></span><br>
                <span>🗺️ <strong>{row['City']}, {row['County']} County</strong></span> &nbsp;&nbsp;
                <span>📞 <strong>{row['Phone']}</strong></span><br>
                <span>💳 <strong>Insurance:</strong> {row['Insurance Accepted']}</span><br>
                <span>✅ <strong>Accreditation:</strong> {row['Accreditation']}</span><br>
                <span>🌐 <strong>Website:</strong> {web_html}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── TABLE ──────────────────────────────────────────────────────────────────────
with tab_table:
    cols = ["Hospital", "County", "City", "Bed Count", "Program Type",
            "Population Served", "Insurance Accepted", "Accreditation",
            "Phone", "Website"]

    st.dataframe(filtered[cols], width="stretch", hide_index=True)

    st.markdown("#### Hospital Detail")
    sel = st.selectbox("Select a hospital for full details",
                       options=filtered["Hospital"].tolist())
    row = filtered[filtered["Hospital"] == sel].iloc[0]

    d1, d2 = st.columns(2)
    with d1:
        st.markdown(f"**Hospital:** {row['Hospital']}")
        st.markdown(f"**Program Type:** {row['Program Type']}")
        st.markdown(f"**Population Served:** {row['Population Served']}")
        st.markdown(f"**Accreditation:** {row['Accreditation']}")
    with d2:
        st.markdown(f"**Address:** {row['Address']}")
        st.markdown(f"**City / County:** {row['City']}, {row['County']} County")
        st.markdown(f"**Phone:** {row['Phone']}")
        st.markdown(f"**Bed Count:** {int(row['Bed Count'])}")
        st.markdown(f"**Insurance Accepted:** {row['Insurance Accepted']}")
        if pd.notna(row["Website"]):
            st.markdown(f"**Website:** {row['Website']}")

# ── MAP ────────────────────────────────────────────────────────────────────────
with tab_map:
    map_df = filtered.dropna(subset=["lat", "lon"]).copy()
    map_df["Bed Count"] = map_df["Bed Count"].fillna(0).astype(int)

    if map_df.empty:
        st.info("No location data available for the current filter selection.")
    else:
        st.markdown(f"**{len(map_df)} hospital{'s' if len(map_df) != 1 else ''} plotted** — circle size reflects bed count")

        # Scale radius: min 3 000 m, scale up with bed count
        map_df["radius"] = (map_df["Bed Count"].clip(lower=20) * 60).clip(upper=80_000)

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position=["lon", "lat"],
            get_radius="radius",
            get_fill_color=[192, 82, 42, 180],
            get_line_color=[120, 40, 10],
            line_width_min_pixels=1,
            pickable=True,
        )

        view = pdk.ViewState(
            latitude=36.7783,
            longitude=-119.4179,
            zoom=5.2,
            pitch=0,
        )

        tooltip = {
            "html": """
                <b>{Hospital}</b><br/>
                🏙️ {City}, {County} County<br/>
                🛏️ <b>{Bed Count}</b> beds<br/>
                📋 {Program Type}<br/>
                👥 {Population Served}<br/>
                📞 {Phone}
            """,
            "style": {
                "backgroundColor": "#1a1a1a",
                "color": "white",
                "fontSize": "13px",
                "padding": "10px",
                "borderRadius": "6px",
                "maxWidth": "320px",
            },
        }

        st.pydeck_chart(
            pdk.Deck(
                layers=[layer],
                initial_view_state=view,
                tooltip=tooltip,
                map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
            ),
            height=560,
        )

        st.markdown("#### Hospitals on Map")
        st.dataframe(
            map_df[["Hospital", "City", "County", "Bed Count", "Program Type", "Phone"]],
            width="stretch",
            hide_index=True,
        )

# ── CHARTS ─────────────────────────────────────────────────────────────────────
with tab_charts:
    ch1, ch2 = st.columns(2)

    with ch1:
        st.markdown("#### Hospitals by County")
        cnty_ct = (filtered.groupby("County")["Hospital"]
                   .count().sort_values(ascending=False)
                   .reset_index().rename(columns={"Hospital": "Count"}))
        st.bar_chart(cnty_ct.set_index("County"), height=350)

    with ch2:
        st.markdown("#### Hospitals by Accreditation")
        acc_series = (filtered["Accreditation"]
                      .str.split(";").explode().str.strip()
                      .value_counts().reset_index())
        acc_series.columns = ["Accreditation", "Count"]
        st.bar_chart(acc_series.set_index("Accreditation"), height=350)

    st.markdown("#### 🛏️ Bed Capacity by County")
    beds_cnty = (filtered.groupby("County")["Bed Count"]
                 .sum().sort_values(ascending=False)
                 .reset_index())
    st.bar_chart(beds_cnty.set_index("County"), height=320)

    st.markdown("#### Hospitals by Program Type")
    prog_series = (filtered["Program Type"]
                   .str.split(";").explode().str.strip()
                   .value_counts().reset_index())
    prog_series.columns = ["Program Type", "Count"]
    st.bar_chart(prog_series.set_index("Program Type"), height=320)

st.markdown("---")
st.caption("Data sourced from provided listings. Verify bed availability, admissions criteria, and insurance coverage directly with each facility.")
