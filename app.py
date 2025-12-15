import streamlit as st
import folium
from streamlit_folium import st_folium
import math

# =================================================
# 페이지 설정
# =================================================
st.set_page_config(layout="wide", page_title="Factory Distance Map")

# =================================================
# 상태 초기화
# =================================================
if "selected_factory" not in st.session_state:
    st.session_state["selected_factory"] = None
if "search" not in st.session_state:
    st.session_state["search"] = ""

# =================================================
# CSS
# =================================================
st.markdown("""
<style>
:root { color-scheme: light !important; }

body, .stApp {
    background-color: white !important;
    color: black !important;
}

.brand-title {
    color: black !important;
    font-weight: 700;
    margin-bottom: 6px;
}

div[data-testid="stCheckbox"] label span {
    color: black !important;
    font-weight: 600;
}

/* 오른쪽 리스트 */
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

.factory-btn {
    width: 100%;
    text-align: left;
    padding: 8px;
    border-radius: 6px;
    border: 1px solid #333;
    margin-bottom: 6px;
    background-color: #1f1f1f;
    color: white;
    cursor: pointer;
}

.factory-btn.selected {
    background-color: #2563eb;
    border-color: #2563eb;
}

.factory-btn:hover {
    background-color: #333;
}

/* 지도 하단 정보 카드 */
.info-card {
    background-color: #f8f9fa;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 16px;
    margin-top: 12px;
    font-size: 16px;
}
.info-card b {
    font-size: 18px;
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
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
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
# 브랜드 선택
# =================================================
st.markdown("<div class='brand-title'>브랜드 선택</div>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    show_nike = st.checkbox("Nike", True)
with c2:
    show_adidas = st.checkbox("Adidas", True)

# 검색
st.session_state.search = st.text_input("공장 검색", st.session_state.search)

visible = [
    f for f in factories
    if ((f[1]=="Nike" and show_nike) or (f[1]=="Adidas" and show_adidas))
    and st.session_state.search.lower() in f[2].lower()
]

selected = st.session_state["selected_factory"]

# =================================================
# 레이아웃
# =================================================
col_map, col_list = st.columns([4, 1])

# =================================================
# 지도
# =================================================
with col_map:
    if selected:
        center = [selected[3], selected[4]]
        zoom = 8
    else:
        center = [-6.6,108.2]
        zoom = 7

    m = folium.Map(location=center, zoom_start=zoom)

    # Ducksan
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
        fid, brand, name, lat, lon, eta = f
        color = "red" if brand == "Nike" else "green"
        folium.Marker(
            [lat, lon],
            popup=f"<b>{name}</b><br>{brand}<br>{eta}",
            icon=folium.Icon(color=color)
        ).add_to(m)

    if selected:
        folium.PolyLine(
            [[DUCKSAN["lat"], DUCKSAN["lon"]],[selected[3], selected[4]]],
            color="black",
            weight=4
        ).add_to(m)

    st_folium(m, height=800, key="map")

    # 지도 하단 정보 카드
    if selected:
        dist = haversine_km(
            DUCKSAN["lat"], DUCKSAN["lon"],
            selected[3], selected[4]
        )
        st.markdown(f"""
        <div class="info-card">
            <b>{selected[2]}</b><br>
            브랜드: {selected[1]}<br>
            거리: {dist:.1f} km<br>
            소요시간: {selected[5]}
        </div>
        """, unsafe_allow_html=True)

# =================================================
# 오른쪽 공장 리스트
# =================================================
with col_list:
    st.markdown("<div class='factory-list'>", unsafe_allow_html=True)
    st.markdown("<h3>공장 리스트</h3>", unsafe_allow_html=True)

    if st.button("전체 공장 보기"):
        st.session_state["selected_factory"] = None

    for f in visible:
        selected_cls = "selected" if selected == f else ""
        st.markdown(
            f"""
            <div class="factory-btn {selected_cls}"
                 onclick="window.location.reload()">
                {f[1]} | {f[2]}
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("select", key=f"btn_{f[0]}"):
            st.session_state["selected_factory"] = f

    st.markdown("</div>", unsafe_allow_html=True)
