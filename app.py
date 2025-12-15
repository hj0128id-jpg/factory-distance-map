import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import Element
import math
import os

# =================================================
# 페이지 설정
# =================================================
st.set_page_config(
    layout="wide",
    page_title="Factory Distance Map"
)

# =================================================
# 상태 초기화
# =================================================
if "selected_factory" not in st.session_state:
    st.session_state["selected_factory"] = None

# =================================================
# CSS (화이트 테마 + 기존 스타일 유지)
# =================================================
st.markdown("""
<style>
:root { color-scheme: light !important; }

body, .stApp {
    background-color: white !important;
    color: black !important;
}

/* 상단 타이틀 */
.header-title {
    font-size: 28px;
    font-weight: 700;
    margin-left: 12px;
}

/* 브랜드 선택 */
.brand-title {
    color: black !important;
    font-weight: 700;
    margin-bottom: 6px;
}

div[data-testid="stCheckbox"] label span {
    color: black !important;
    font-weight: 600;
}

/* 오른쪽 공장 리스트 */
.factory-list {
    background-color: #111;
    color: white;
    padding: 12px;
    border-radius: 8px;
    height: 100%;
}

.factory-list h3 {
    color: white;
}

.factory-list button {
    width: 100%;
    text-align: left;
    color: white !important;
    background-color: #1f1f1f;
    border: 1px solid #333;
    margin-bottom: 6px;
}

.factory-list button:hover {
    background-color: #333;
}
</style>
""", unsafe_allow_html=True)

# =================================================
# 상단 헤더 (회사 로고 + 타이틀)
# =================================================
h1, h2 = st.columns([1, 6])
with h1:
    if os.path.exists("company_logo.png"):
        st.image("company_logo.png", width=240)
with h2:
    st.markdown("<div class='header-title'>Factory Distance Map</div>", unsafe_allow_html=True)

st.markdown("---")

# =================================================
# 거리 계산
# =================================================
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

# =================================================
# 브랜드 로고 매핑
# =================================================
def brand_logo(brand):
    if brand == "Nike":
        return "logo_nike.png"
    if brand == "Adidas":
        return "logo_adidas.png"
    return None

# =================================================
# Ducksan
# =================================================
DUCKSAN = {
    "name": "Ducksan Factory",
    "lat": -6.385298062386163,
    "lon": 107.24043447439371,
}

# =================================================
# 공장 데이터
# =================================================
factories = [
    (1,"Nike","IY.PIC Nikomas Nike, Adidas",-6.16276739755951,106.31671924330799,"130 min (135km)"),
    (2,"Nike","IA.Adis",-6.198360928194161,106.45490204318438,"120 min (117km)"),
    (3,"Nike","JV Victory",-6.177442951766401,106.53013303741062,"130 min (121km)"),
    (4,"Nike","RH Ching Luh",-6.174073195725205,106.53745401501386,"130 min (113km)"),
    (5,"Nike","IM KMK",-6.204102530389127,106.50946954319025,"125 min (117km)"),
    (6,"Nike","IR Pratama",-6.2353570645495,106.64156261937526,"97 min (96.2km)"),
    (7,"Nike","JJ Changshin",-6.3662150106528985,107.3754476465168,"37 min (23.3km)"),
    (8,"Nike","TT Tekwang",-6.557840458416882,107.78753277093949,"76 min (80km)"),
    (9,"Nike","J2 Shoetown",-6.668837588760989,108.26586454850877,"124 min (150km)"),
    (10,"Nike","PM Sumber masanda",-6.867241347419877,108.98398073674508,"180 min (234km)"),

    (15,"Adidas","PWI-1 Parkland",-6.18005569680193,106.34344218683786,"420 min (487km)"),
    (18,"Adidas","PBB Bintang Indo",-6.867770507966313,108.84263889750521,"167 min (207km)"),
    (21,"Adidas","PWI-3 Parkland",-6.867770507966313,108.84263889750521,"312 min (416km)")
]

# =================================================
# 브랜드 선택 (로고 포함)
# =================================================
st.markdown("<div class='brand-title'>브랜드 선택</div>", unsafe_allow_html=True)

b1, b2 = st.columns(2)
with b1:
    st.image("logo_nike.png", width=60)
    show_nike = st.checkbox("Nike", True)
with b2:
    st.image("logo_adidas.png", width=60)
    show_adidas = st.checkbox("Adidas", True)

visible = [
    f for f in factories
    if (f[1] == "Nike" and show_nike) or (f[1] == "Adidas" and show_adidas)
]

selected = st.session_state["selected_factory"]

# =================================================
# 레이아웃
# =================================================
col_map, col_list = st.columns([4, 1])

# =================================================
# 지도 (지금 네가 만족한 그대로 유지)
# =================================================
with col_map:
    m = folium.Map(
        location=[-6.6, 108.2],
        zoom_start=7
    )

    folium.CircleMarker(
        [DUCKSAN["lat"], DUCKSAN["lon"]],
        radius=8,
        color="blue",
        fill=True,
        fill_color="blue",
        popup="Ducksan Factory"
    ).add_to(m)

    targets = [selected] if selected else visible

    for f in targets:
        fid, brand, name, lat, lon, eta = f
        color = "red" if brand == "Nike" else "green"
        folium.Marker(
            [lat, lon],
            popup=f"<b>{name}</b><br>{brand}<br>{eta}",
            icon=folium.Icon(color=color)
        ).add_to(m)

    if selected:
        dist = haversine_km(DUCKSAN["lat"], DUCKSAN["lon"], selected[3], selected[4])

        folium.PolyLine(
            [[DUCKSAN["lat"], DUCKSAN["lon"]],[selected[3], selected[4]]],
            color="black",
            weight=4
        ).add_to(m)

        logo = brand_logo(selected[1])

        info_html = f"""
        <div style="
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            background: rgba(255,255,255,0.95);
            padding: 14px 18px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            min-width: 260px;
        ">
            <img src="{logo}" width="70"><br><br>
            <b>{selected[2]}</b><br>
            브랜드: {selected[1]}<br>
            거리: {dist:.1f} km<br>
            소요시간: {selected[5]}
        </div>
        """
        m.get_root().html.add_child(Element(info_html))

    st_folium(m, height=700, width=1400, key="map")

# =================================================
# 오른쪽 공장 리스트
# =================================================
with col_list:
    st.markdown("<div class='factory-list'>", unsafe_allow_html=True)
    st.markdown("<h3>공장 리스트</h3>", unsafe_allow_html=True)

    if st.button("전체 공장 보기"):
        st.session_state["selected_factory"] = None

    for f in visible:
        if st.button(f"{f[1]} | {f[2]}", key=f"btn_{f[0]}"):
            st.session_state["selected_factory"] = f

    st.markdown("</div>", unsafe_allow_html=True)
