import streamlit as st
import folium
from streamlit_folium import st_folium
import math

# ===============================
# 페이지 설정 + 화이트 테마 강제
# ===============================
st.set_page_config(layout="wide", page_title="Factory Map")

st.markdown("""
<style>
body, .stApp {
    background-color: white !important;
    color: black !important;
}
.stCheckbox label {
    color: black !important;
    font-weight: 600;
}
.factory-item {
    padding: 8px 6px;
    border-bottom: 1px solid #ddd;
    cursor: pointer;
}
.factory-item:hover {
    background-color: #f2f2f2;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# 거리 계산 함수
# ===============================
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# ===============================
# Ducksan 공장
# ===============================
DUCKSAN = {
    "name": "Ducksan Factory",
    "lat": -6.385298062386163,
    "lon": 107.24043447439371,
}

# ===============================
# 공장 데이터 (네가 준 그대로)
# ===============================
factories = [
    # Nike
    (1, "Nike", "IY.PIC Nikomas Nike, Adidas", -6.16276739755951, 106.31671924330799, "130 min (135km)"),
    (2, "Nike", "IA.Adis", -6.198360928194161, 106.45490204318438, "120 min (117km)"),
    (3, "Nike", "JV Victory", -6.177442951766401, 106.53013303741062, "130 min (121km)"),
    (4, "Nike", "RH Ching Luh", -6.174073195725205, 106.53745401501386, "130 min (113km)"),
    (5, "Nike", "IM KMK", -6.204102530389127, 106.50946954319025, "125 min (117km)"),
    (6, "Nike", "IR Pratama", -6.2353570645495, 106.64156261937526, "97 min (96.2km)"),
    (7, "Nike", "JJ Changshin", -6.3662150106528985, 107.3754476465168, "37 min (23.3km)"),
    (8, "Nike", "TT Tekwang", -6.557840458416882, 107.78753277093949, "76 min (80km)"),
    (9, "Nike", "J2 Shoetown", -6.668837588760989, 108.26586454850877, "124 min (150km)"),
    (10, "Nike", "PM Sumber masanda", -6.867241347419877, 108.98398073674508, "180 min (234km)"),
    (11, "Nike", "SCI Selalu Cinta", -7.3649526370117275, 110.50302727705107, "317 min (442km)"),
    (12, "Nike", "RY.JJS Changshin", -7.074890966054376, 108.07273203695073, "160 min (152km)"),
    (13, "Nike", "RY Pou Yuen", -6.803464029220425, 107.22441150566885, "128 min (72km)"),
    (14, "Nike", "JX Pratama", -6.86320705203383, 107.02668764100862, "173 min (90km)"),

    # Adidas
    (15, "Adidas", "PWI-1 Parkland", -6.18005569680193, 106.34344218683786, "420 min (487km)"),
    (16, "Adidas", "IY.PIC Nikomas Nike, Adidas", -6.16276739755951, 106.31671924330799, "130 min (135km)"),
    (17, "Adidas", "PRB Panarub", -6.170607657812733, 106.6191471209852, "105 min (107km)"),
    (18, "Adidas", "PBB Bintang Indo", -6.867770507966313, 108.84263889750521, "167 min (207km)"),
    (19, "Adidas", "SHI Tah Sung Hung", -6.929972278573358, 108.87605444522376, "167 min (220km)"),
    (20, "Adidas", "HWI Hwa Seung", -6.712188897782861, 110.72403180338068, "360 min (455km)"),
    (21, "Adidas", "PWI-3 Parkland", -6.867770507966313, 108.84263889750521, "312 min (416km)"),
    (22, "Adidas", "PWI-4 Parkland", -6.7142319309820175, 111.38549046857136, "362 min (458km)"),
    (23, "Adidas", "HWI-2 Hwa Seung", -6.712771739449992, 111.19681124717319, "420 min (500km)"),
    (24, "Adidas", "PWi-5 Parkland", -6.709008772441859, 111.39741373178808, "447 min (522km)"),
    (25, "Adidas", "PGS Pouchen", -6.875398775012465, 107.02241821336372, "180 min (93km)"),
    (26, "Adidas", "PGD.PGD2 Glostar Newbal, Adidas", -6.974318300905597, 106.83196261494169, "153 min (138km)")
]

# ===============================
# 브랜드 필터
# ===============================
col_a, col_b = st.columns(2)
with col_a:
    show_nike = st.checkbox("Nike", True)
with col_b:
    show_adidas = st.checkbox("Adidas", True)

# ===============================
# 레이아웃 (지도 | 리스트)
# ===============================
col_map, col_list = st.columns([4, 1])

# ===============================
# 지도 생성
# ===============================
with col_map:
    m = folium.Map(location=[-6.6, 108.2], zoom_start=7)

    # Ducksan
    folium.CircleMarker(
        [DUCKSAN["lat"], DUCKSAN["lon"]],
        radius=8,
        color="blue",
        fill=True,
        fill_color="blue",
        popup=DUCKSAN["name"],
    ).add_to(m)

    # 공장 마커
    visible_factories = []
    for f in factories:
        fid, brand, name, lat, lon, eta = f
        if (brand == "Nike" and show_nike) or (brand == "Adidas" and show_adidas):
            visible_factories.append(f)
            folium.Marker(
                [lat, lon],
                popup=f"<b>{name}</b><br>{brand}<br>{eta}",
                icon=folium.Icon(color="red"),
            ).add_to(m)

    map_state = st_folium(m, height=900, width=1100)

# ===============================
# 오른쪽 공장 리스트
# ===============================
with col_list:
    st.markdown("### 공장 리스트")

    for f in visible_factories:
        fid, brand, name, lat, lon, eta = f

        if st.button(f"{brand} | {name}", key=f"btn_{fid}"):
            dist = haversine_km(DUCKSAN["lat"], DUCKSAN["lon"], lat, lon)

            m2 = folium.Map(location=[lat, lon], zoom_start=8)

            folium.CircleMarker(
                [DUCKSAN["lat"], DUCKSAN["lon"]],
                radius=8,
                color="blue",
                fill=True,
                fill_color="blue",
                popup=DUCKSAN["name"],
            ).add_to(m2)

            folium.Marker(
                [lat, lon],
                popup=f"<b>{name}</b><br>{brand}<br>{eta}<br>{dist:.1f} km",
                icon=folium.Icon(color="red"),
            ).add_to(m2)

            folium.PolyLine(
                [[DUCKSAN["lat"], DUCKSAN["lon"]], [lat, lon]],
                color="black",
                weight=4,
            ).add_to(m2)

            st.markdown(f"**거리:** {dist:.1f} km")
            st.markdown(f"**소요시간:** {eta}")

            st_folium(m2, height=900, width=1100)
