import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import Element
import math

# =================================================
# 페이지 설정
# =================================================
st.set_page_config(
    layout="wide",
    page_title="Factory Distance Map"
)

# =================================================
# 상태
# =================================================
if "selected_factory" not in st.session_state:
    st.session_state.selected_factory = None

# =================================================
# CSS (화이트 테마 + 레이아웃 고정)
# =================================================
st.markdown("""
<style>
:root { color-scheme: light !important; }

body, .stApp {
    background-color: white !important;
    color: black !important;
}

/* 제목 영역 */
.header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 12px;
}

/* 브랜드 선택 */
.brand-box {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
}

div[data-testid="stCheckbox"] label span {
    color: black !important;
    font-weight: 600;
}

/* 공장 리스트 박스 */
.factory-list {
    background: #111;
    color: white;
    padding: 12px;
    border-radius: 10px;
    height: 700px;
    overflow-y: auto;
}

.factory-list h3 {
    color: white;
    margin-bottom: 10px;
}

.factory-list button {
    width: 100%;
    text-align: left;
    background: #1f1f1f;
    color: white !important;
    border: 1px solid #333;
    margin-bottom: 6px;
}

.factory-list button:hover {
    background: #333;
}
</style>
""", unsafe_allow_html=True)

# =================================================
# 거리 계산
# =================================================
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(dlon / 2) ** 2
    )
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# =================================================
# Ducksan
# =================================================
DUCKSAN = {
    "name": "Ducksan Factory",
    "lat": -6.385298062386163,
    "lon": 107.24043447439371,
}

# =================================================
# 공장 데이터 (전체)
# =================================================
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
    (26, "Adidas", "PGD Glostar", -6.974318300905597, 106.83196261494169, "153 min (138km)"),

    # New Balance
    (27, "New Balance", "PWI-2 Parkland", -6.164065615736655, 106.34362393191581, "127 min (134km)"),
    (28, "New Balance", "MPI Metro Pearl", -6.553123695397186, 107.43167326062274, "57 min (51km)"),
    (29, "New Balance", "PGD2 Glostar", -6.974318300905597, 106.83196261494169, "153 min (138km)"),

    # Puma
    (30, "Puma", "IDM Diamond", -6.760451512559341, 108.26909332164612, "124 min (151km)"),

    # Under Armour
    (31, "Under Armour", "Dean Shoes", -6.391000160605475, 107.39562888401743, "43 min (29km)"),
    (32, "Under Armour", "Long Rich", -6.8755937402321985, 108.775905329925, "150 min (200km)"),

    # Converse
    (33, "Converse", "SJI Shoenary", -7.369617174917486, 110.22038960678333, "350 min (460km)"),

    # Decathlon
    (34, "Decathlon", "DPS-2 Dwi Prima", -7.398359508521098, 111.50982327782442, "398 min (567km)"),

    # Yonex
    (35, "Yonex", "DPS Dwi Prima", -7.505210694143256, 111.65093697468592, "405 min (591km)"),

    # Sperry
    (36, "Sperry", "WWW Young Tree", -7.565685915234356, 110.76484773866882, "360 min (482km)")
]

# =================================================
# 헤더
# =================================================
st.markdown("""
<div class="header">
    <img src="company_logo.png" height="48">
    <h1>Factory Distance Map</h1>
</div>
""", unsafe_allow_html=True)

# =================================================
# 브랜드 필터
# =================================================
brands = sorted(set(f[1] for f in factories))
brand_check = {}

cols = st.columns(len(brands))
for col, brand in zip(cols, brands):
    with col:
        brand_check[brand] = st.checkbox(brand, True)

visible = [f for f in factories if brand_check.get(f[1], False)]
selected = st.session_state.selected_factory

# =================================================
# 레이아웃
# =================================================
col_map, col_list = st.columns([5, 2])

# =================================================
# 지도 (고정 크기)
# =================================================
with col_map:
    m = folium.Map(
        location=[-6.6, 108.2],
        zoom_start=7,
        control_scale=True
    )

    folium.CircleMarker(
        [DUCKSAN["lat"], DUCKSAN["lon"]],
        radius=8,
        color="blue",
        fill=True,
        fill_color="blue",
        popup=DUCKSAN["name"]
    ).add_to(m)

    targets = [selected] if selected else visible

    for f in targets:
        folium.Marker(
            [f[3], f[4]],
            popup=f"<b>{f[2]}</b><br>{f[1]}<br>{f[5]}",
            icon=folium.Icon(color="red")
        ).add_to(m)

    if selected:
        dist = haversine_km(
            DUCKSAN["lat"], DUCKSAN["lon"],
            selected[3], selected[4]
        )

        folium.PolyLine(
            [[DUCKSAN["lat"], DUCKSAN["lon"]],[selected[3], selected[4]]],
            color="black",
            weight=4
        ).add_to(m)

        info = f"""
        <div style="
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            padding: 14px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,.15);
            z-index: 9999;
        ">
            <b>{selected[2]}</b><br>
            브랜드: {selected[1]}<br>
            거리: {dist:.1f} km<br>
            소요시간: {selected[5]}
        </div>
        """
        m.get_root().html.add_child(Element(info))

    st_folium(
        m,
        height=700,
        width=1400,
        key="map"
    )

# =================================================
# 공장 리스트 (스크롤 박스)
# =================================================
with col_list:
    st.markdown("<div class='factory-list'>", unsafe_allow_html=True)
    st.markdown("<h3>공장 리스트</h3>", unsafe_allow_html=True)

    if st.button("전체 공장 보기"):
        st.session_state.selected_factory = None

    for f in visible:
        if st.button(f"{f[1]} | {f[2]}", key=f"btn_{f[0]}"):
            st.session_state.selected_factory = f

    st.markdown("</div>", unsafe_allow_html=True)
