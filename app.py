import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import Element
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

# =================================================
# CSS (화이트 테마 강제)
# =================================================
st.markdown("""
<style>
:root { color-scheme: light !important; }

body, .stApp {
    background-color: white !important;
    color: black !important;
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
# 공장 데이터 (전체)
# =================================================
factories = [
    # Nike
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
    (11,"Nike","SCI Selalu Cinta",-7.3649526370117275,110.50302727705107,"317 min (442km)"),
    (12,"Nike","RY.JJS Changshin",-7.074890966054376,108.07273203695073,"160 min (152km)"),
    (13,"Nike","RY Pou Yuen",-6.803464029220425,107.22441150566885,"128 min (72km)"),
    (14,"Nike","JX Pratama",-6.86320705203383,107.02668764100862,"173 min (90km)"),

    # Adidas
    (15,"Adidas","PWI-1 Parkland",-6.18005569680193,106.34344218683786,"420 min (487km)"),
    (16,"Adidas","IY.PIC Nikomas Nike, Adidas",-6.16276739755951,106.31671924330799,"130 min (135km)"),
    (17,"Adidas","PRB Panarub",-6.170607657812733,106.6191471209852,"105 min (107km)"),
    (18,"Adidas","PBB Bintang Indo",-6.867770507966313,108.84263889750521,"167 min (207km)"),
    (19,"Adidas","SHI Tah Sung Hung",-6.929972278573358,108.87605444522376,"167 min (220km)"),
    (20,"Adidas","HWI Hwa Seung",-6.712188897782861,110.72403180338068,"360 min (455km)"),
    (21,"Adidas","PWI-3 Parkland",-6.867770507966313,108.84263889750521,"312 min (416km)"),
    (22,"Adidas","PWI-4 Parkland",-6.7142319309820175,111.38549046857136,"362 min (458km)"),
    (23,"Adidas","HWI-2 Hwa Seung",-6.712771739449992,111.19681124717319,"420 min (500km)"),
    (24,"Adidas","PWi-5 Parkland",-6.709008772441859,111.39741373178808,"447 min (522km)"),
    (25,"Adidas","PGS Pouchen",-6.875398775012465,107.02241821336372,"180 min (93km)"),
    (26,"Adidas","PGD.PGD2 Glostar Newbal, Adidas",-6.974318300905597,106.83196261494169,"153 min (138km)")
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
# 지도
# =================================================
with col_map:
    if selected:
        center = [selected[3], selected[4]]
        zoom = 4
    else:
        center = [-6.6, 108.2]
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

    # 경로 + 정보 오버레이
    if selected:
        dist = haversine_km(
            DUCKSAN["lat"], DUCKSAN["lon"],
            selected[3], selected[4]
        )

        folium.PolyLine(
            [[DUCKSAN["lat"], DUCKSAN["lon"]], [selected[3], selected[4]]],
            color="black",
            weight=4
        ).add_to(m)

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
            font-size: 14px;
            min-width: 240px;
        ">
            <b style="font-size:16px;">{selected[2]}</b><br>
            브랜드: {selected[1]}<br>
            거리: {dist:.1f} km<br>
            소요시간: {selected[5]}
        </div>
        """
        m.get_root().html.add_child(Element(info_html))

    st_folium(
        m,
        height=1050,
        width=1400,
        key="map"
    )

# =================================================
# 오른쪽 공장 리스트
# =================================================
with col_list:
    st.markdown("<div class='factory-list'>", unsafe_allow_html=True)
    st.markdown("<h3>공장 리스트</h3>", unsafe_allow_html=True)

    if st.button("전체 공장 보기"):
        st.session_state["selected_factory"] = None

    for f in visible:
        fid, brand, name, lat, lon, eta = f
        if st.button(f"{brand} | {name}", key=f"btn_{fid}"):
            st.session_state["selected_factory"] = f

    st.markdown("</div>", unsafe_allow_html=True)
