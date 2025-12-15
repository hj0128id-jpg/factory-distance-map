# app.py
import streamlit as st
import pandas as pd
import pydeck as pdk
import math
import requests

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Factory Distance Map", layout="wide")

# 우리 공장 좌표 (출발지)
MY_FACTORY = {
    "name": "Our Factory (Ducksan)",
    "lat": -6.385298062386163,
    "lon": 107.24043447439371
}

# ----------------- 데이터 (원본명 그대로) -----------------
# Shoes: Nike / Adidas (IY.PIC Nikomas appears in both)
data_rows = [
    # Nike block (from your table)
    ("Nike", "IY.PIC Nikomas Nike, Adidas", -6.16276739755951, 106.31671924330799),
    ("Nike", "IA.Adis", -6.198360928194161, 106.45490204318438),
    ("Nike", "JV Victory", -6.177442951766401, 106.53013303741062),
    ("Nike", "RH Ching Luh", -6.174073195725205, 106.53745401501386),
    ("Nike", "IM KMK", -6.204102530389127, 106.50946954319025),
    ("Nike", "IR Pratama", -6.2353570645495, 106.64156261937526),
    ("Nike", "JJ Changshin", -6.3662150106528985, 107.3754476465168),
    ("Nike", "TT Tekwang", -6.557840458416882, 107.78753277093949),
    ("Nike", "J2 Shoetown", -6.668837588760989, 108.26586454850877),
    ("Nike", "PM Sumber masanda", -6.867241347419877, 108.98398073674508),
    ("Nike", "SCI Selalu Cinta", -7.3649526370117275, 110.50302727705107),
    ("Nike", "RY.JJS Changshin", -7.074890966054376, 108.07273203695073),
    ("Nike", "RY Pou Yuen", -6.803464029220425, 107.22441150566885),
    ("Nike", "JX Pratama", -6.86320705203383, 107.02668764100862),

    # Adidas block
    ("Adidas", "PWI-1 Parkland", -6.18005569680193, 106.34344218683786),
    ("Adidas", "IY.PIC Nikomas Nike, Adidas", -6.16276739755951, 106.31671924330799),  # same name appears in both
    ("Adidas", "PRB Panarub", -6.170607657812733, 106.6191471209852),
    ("Adidas", "PBB Bintang Indo", -6.867770507966313, 108.84263889750521),
    ("Adidas", "SHI Tah Sung Hung", -6.929972278573358, 108.87605444522376),
    ("Adidas", "HWI Hwa Seung", -6.712188897782861, 110.72403180338068),
    ("Adidas", "PWI-3 Parkland", -6.634589345449244, 110.41133627660086),
    ("Adidas", "PWI-4 Parkland", -6.7142319309820175, 111.38549046857136),
    ("Adidas", "HWI-2 Hwa Seung", -6.712771739449992, 111.19681124717319),
    ("Adidas", "PWi-5 Parkland", -6.709008772441859, 111.39741373178808),
    ("Adidas", "PGS Pouchen", -6.875398775012465, 107.02241821336372),
    ("Adidas", "PGD.PGD2 Glostar Newbal, Adidas", -6.974318300905597, 106.83196261494169),
]

df = pd.DataFrame(data_rows, columns=["brand", "name", "lat", "lon"])

# ----------------- 사이드바: Google API 키 입력 (선택) -----------------
st.sidebar.title("Settings")
GOOGLE_API_KEY = st.sidebar.text_input("Google Distance Matrix API Key (optional)", type="password")
avg_speed_kmh = st.sidebar.number_input("Average speed for ETA when API not set (km/h)", value=40.0, min_value=10.0)

# ----------------- 상단: 로고 + 브랜드 선택 -----------------
col_left, col_right = st.columns([1, 2])
with col_left:
    #st.image("company_logo.png", width=140)  # 파일명 바꿔도 됨

with col_right:
    st.markdown("## Client Factories — Shoes")
    st.markdown("Select brand and a factory to see distance & ETA from our factory.")

brand_choice = st.selectbox("Brand", ["Nike", "Adidas"])

# filter by brand
brand_df = df[df["brand"] == brand_choice].reset_index(drop=True)

st.write(f"### {brand_choice} factories ({len(brand_df)})")
st.dataframe(brand_df[["name", "lat", "lon"]].rename(columns={"name":"Factory Name","lat":"LAT","lon":"LNG"}), height=250)

# ----------------- 공장 선택 인터페이스 -----------------
selected_name = st.selectbox("Select a factory (click to show on map & calc distance):", brand_df["name"].tolist())

selected_row = brand_df[brand_df["name"] == selected_name].iloc[0]
dest_lat, dest_lon = selected_row["lat"], selected_row["lon"]

# ----------------- 거리 계산 함수 -----------------
def haversine_km(lat1, lon1, lat2, lon2):
    # returns distance in kilometers (great-circle)
    R = 6371.0  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def google_distance_matrix(api_key, origin_lat, origin_lon, dest_lat, dest_lon):
    # returns (distance_text, distance_meters, duration_text, duration_seconds) or None on error
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": f"{origin_lat},{origin_lon}",
        "destinations": f"{dest_lat},{dest_lon}",
        "key": api_key,
        "mode": "driving",
        "language": "en"
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        if data.get("status") == "OK" and data.get("rows"):
            element = data["rows"][0]["elements"][0]
            if element.get("status") == "OK":
                dist_text = element["distance"]["text"]
                dist_m = element["distance"]["value"]
                dur_text = element["duration"]["text"]
                dur_s = element["duration"]["value"]
                return dist_text, dist_m, dur_text, dur_s
    except Exception as e:
        # fail silently to fallback
        print("Google API error:", e)
    return None

# ----------------- 계산 및 출력 -----------------
st.markdown("---")
st.subheader("Selected Factory")
st.write(f"**{selected_name}**  —  LAT: {dest_lat}, LNG: {dest_lon}")

# try Google first if key provided
google_result = None
if GOOGLE_API_KEY:
    with st.spinner("Querying Google Distance Matrix..."):
        google_result = google_distance_matrix(GOOGLE_API_KEY, MY_FACTORY["lat"], MY_FACTORY["lon"], dest_lat, dest_lon)

if google_result:
    dist_text, dist_m, dur_text, dur_s = google_result
    st.success("Distance & ETA (Google Distance Matrix)")
    st.write(f"- Distance: **{dist_text}** ({dist_m/1000:.2f} km)")
    st.write(f"- Estimated travel time: **{dur_text}** ({dur_s//60} min)")
else:
    # fallback: haversine + simple ETA estimate
    dist_km = haversine_km(MY_FACTORY["lat"], MY_FACTORY["lon"], dest_lat, dest_lon)
    eta_min = (dist_km / max(1e-6, avg_speed_kmh)) * 60.0
    st.warning("Google API not used or failed — showing approximate (great-circle) distance & estimated time.")
    st.write(f"- Approx distance (straight-line): **{dist_km:.2f} km**")
    st.write(f"- Estimated travel time (at {avg_speed_kmh} km/h): **{eta_min:.0f} min**")

# ----------------- 지도: 우리공장 + 선택 공장 표시 -----------------
map_df = pd.DataFrame([
    {"name": MY_FACTORY["name"], "lat": MY_FACTORY["lat"], "lon": MY_FACTORY["lon"], "type": "Our Factory"},
    {"name": selected_name, "lat": dest_lat, "lon": dest_lon, "type": "Client Factory"},
])

layer = pdk.Layer(
    "ScatterplotLayer",
    data=map_df,
    get_position='[lon, lat]',
    get_fill_color='[255, 0, 0] if type == "Our Factory" else [0, 120, 255]',
    get_radius=300,
    pickable=True,
)

# If Google returned a driving route (we didn't request route polyline here),
# we still show two pins and a simple connecting line via PathLayer (straight)
path_layer = pdk.Layer(
    "PathLayer",
    data=[{"path": [[MY_FACTORY["lon"], MY_FACTORY["lat"]], [dest_lon, dest_lat]], "name": "route"}],
    get_path="path",
    get_width=4,
)

view_state = pdk.ViewState(latitude=(MY_FACTORY["lat"]+dest_lat)/2, longitude=(MY_FACTORY["lon"]+dest_lon)/2, zoom=7)

tooltip = {"html": "<b>{name}</b><br/>{type}", "style": {"color": "white"}}

st.pydeck_chart(pdk.Deck(layers=[layer, path_layer], initial_view_state=view_state, tooltip=tooltip))

# ----------------- 추가 정보 및 다운로드 -----------------
st.markdown("---")
st.write("You can download the current brand's factory list:")
csv = brand_df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, file_name=f"{brand_choice}_factories.csv", mime="text/csv")
