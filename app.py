import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import Element
import math
import base64

# =================================================
# 기본 설정
# =================================================
st.set_page_config(layout="wide", page_title="Factory Distance Map")

if "selected_factory" not in st.session_state:
    st.session_state["selected_factory"] = None

# =================================================
# CSS
# =================================================
st.markdown("""
<style>
:root { color-scheme: light; }

body, .stApp {
    background-color: white;
    color: black;
}

/* 브랜드 영역 */
.brand-box {
    display: flex;
    gap: 24px;
    align-items: center;
    margin-bottom: 12px;
}

.brand-item {
    display: flex;
    align-items: center;
    gap: 6px;
}

/* 공장 리스트 */
.factory-list {
    height: 700px;
    overflow-y: auto;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 10px;
}

.factory-list button {
    width: 100%;
    text-align: left;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)

# =================================================
# 유틸
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

def img_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# =================================================
# 로고
# =================================================
company_logo = img_b64("company_logo.png")

brand_logos = {
    "Nike": img_b64("logo_nike.png"),
    "Adidas": img_b64("logo_adidas.png"),
    "New Balance": img_b64("logo_newbalance.png"),
    "Puma": img_b64("logo_puma.png"),
    "Converse": img_b64("logo_converse.png"),
    "Decathlon": img_b64("logo_decathlon.png"),
    "Under Armour": img_b64("logo_underarmour.png"),
    "Yonex": img_b64("logo_yonex.png"),
    "Sperry": img_b64("logo_sperry.png"),
}

# =================================================
# 상단 헤더
# =================================================
st.markdown(
    f"""
    <div style="display:flex; align-items:center; gap:20px;">
        <img src="data:image/png;base64,{company_logo}" height="60">
        <h1>Factory Distance Map</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# =================================================
# 브랜드 선택
# =================================================
st.markdown("### 브랜드 선택")

brand_checks = {}
cols = st.columns(5)

for i, brand in enumerate(brand_logos.keys()):
    with cols[i % 5]:
        brand_checks[brand] = st.checkbox(
            brand,
            True,
            label_visibility="collapsed"
        )
        st.image(f"logo_{brand.lower().replace(' ','')}.png", width=70)

# =================================================
# 공장 데이터 (전부 유지)
# =================================================
factories = [
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import Element
import math
import base64

# =================================================
# 기본 설정
# =================================================
st.set_page_config(layout="wide", page_title="Factory Distance Map")

if "selected_factory" not in st.session_state:
    st.session_state["selected_factory"] = None

# =================================================
# CSS
# =================================================
st.markdown("""
<style>
:root { color-scheme: light; }

body, .stApp {
    background-color: white;
    color: black;
}

/* 브랜드 영역 */
.brand-box {
    display: flex;
    gap: 24px;
    align-items: center;
    margin-bottom: 12px;
}

.brand-item {
    display: flex;
    align-items: center;
    gap: 6px;
}

/* 공장 리스트 */
.factory-list {
    height: 700px;
    overflow-y: auto;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 10px;
}

.factory-list button {
    width: 100%;
    text-align: left;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)

# =================================================
# 유틸
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

def img_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# =================================================
# 로고
# =================================================
company_logo = img_b64("company_logo.png")

brand_logos = {
    "Nike": img_b64("logo_nike.png"),
    "Adidas": img_b64("logo_adidas.png"),
    "New Balance": img_b64("logo_newbalance.png"),
    "Puma": img_b64("logo_puma.png"),
    "Converse": img_b64("logo_converse.png"),
    "Decathlon": img_b64("logo_decathlon.png"),
    "Under Armour": img_b64("logo_underarmour.png"),
    "Yonex": img_b64("logo_yonex.png"),
    "Sperry": img_b64("logo_sperry.png"),
}

# =================================================
# 상단 헤더
# =================================================
st.markdown(
    f"""
    <div style="display:flex; align-items:center; gap:20px;">
        <img src="data:image/png;base64,{company_logo}" height="60">
        <h1>Factory Distance Map</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# =================================================
# 브랜드 선택
# =================================================
st.markdown("### 브랜드 선택")

brand_checks = {}
cols = st.columns(5)

for i, brand in enumerate(brand_logos.keys()):
    with cols[i % 5]:
        brand_checks[brand] = st.checkbox(
            brand,
            True,
            label_visibility="collapsed"
        )
        st.image(f"logo_{brand.lower().replace(' ','')}.png", width=70)

# =================================================
# 공장 데이터 (전부 유지)
# =================================================
factories = [
    (1,"Nike","IY.PIC Nikomas Nike, Adidas",-6.16276739755951,106.31671924330799,"130 min (135km)"),
    (2,"Nike","IA.Adis",-6.198360928194161,106.45490204318438,"120 min (117km)"),
    (3,"Nike","JV Victory",-6.177442951766401,106.53013303741062,"130 min (121km)"),
    (4,"Nike","RH Ching Luh",-6.174073195725205,106.53745401501386,"130 min (113km)"),
    (15,"Adidas","PWI-1 Parkland",-6.18005569680193,106.34344218683786,"420 min (487km)"),
    (27,"New Balance","PWI-2 Parkland",-6.164065615736655,106.34362393191581,"127 min (134km)"),
    (30,"Puma","IDM Diamond",-6.760451512559341,108.26909332164612,"124 min (151km)"),
    (31,"Under Armour","Dean Shoes",-6.391000160605475,107.39562888401743,"43 min (29km)"),
    (33,"Converse","SJI Shoenary",-7.369617174917486,110.22038960678333,"350 min (460km)"),
    (34,"Decathlon","DPS-2 Dwi Prima",-7.398359508521098,111.50982327782442,"398 min (567km)"),
    (35,"Yonex","DPS Dwi Prima",-7.505210694143256,111.65093697468592,"405 min (591km)"),
    (36,"Sperry","WWW Young Tree",-7.565685915234356,110.76484773866882,"360 min (482km)")
]

visible = [f for f in factories if brand_checks.get(f[1], False)]

# =================================================
# 메인 레이아웃 (지도 | 공장리스트)
# =================================================
col_map, col_list = st.columns([4, 1])

# ================= 지도 =================
with col_map:
    m = folium.Map(location=[-6.6,108.2], zoom_start=7)

    for f in visible:
        folium.Marker(
            [f[3], f[4]],
            popup=f"{f[2]}<br>{f[5]}"
        ).add_to(m)

    st_folium(m, height=700, width=1400)

# ================= 공장 리스트 =================
with col_list:
    st.markdown("### 공장 리스트")
    st.markdown('<div class="factory-list">', unsafe_allow_html=True)

    for f in visible:
        if st.button(f"{f[1]} | {f[2]}", key=f"f_{f[0]}"):
            st.session_state["selected_factory"] = f

    st.markdown("</div>", unsafe_allow_html=True)

]

visible = [f for f in factories if brand_checks.get(f[1], False)]

# =================================================
# 메인 레이아웃 (지도 | 공장리스트)
# =================================================
col_map, col_list = st.columns([4, 1])

# ================= 지도 =================
with col_map:
    m = folium.Map(location=[-6.6,108.2], zoom_start=7)

    for f in visible:
        folium.Marker(
            [f[3], f[4]],
            popup=f"{f[2]}<br>{f[5]}"
        ).add_to(m)

    st_folium(m, height=700, width=1400)

# ================= 공장 리스트 =================
with col_list:
    st.markdown("### 공장 리스트")
    st.markdown('<div class="factory-list">', unsafe_allow_html=True)

    for f in visible:
        if st.button(f"{f[1]} | {f[2]}", key=f"f_{f[0]}"):
            st.session_state["selected_factory"] = f

    st.markdown("</div>", unsafe_allow_html=True)
