import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import Element
import math
import base64

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
    st.session_state["selected_factory"] = None

# =================================================
# 유틸
# =================================================
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

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
# 로고 (⚠️ 전부 소문자 파일명)
# =================================================
COMPANY_LOGO = img_to_base64("company_logo.png")

BRAND_LOGOS = {
    "Nike": img_to_base64("logo_nike.png"),
    "Adidas": img_to_base64("logo_adidas.png"),
    "New Balance": img_to_base64("logo_newbalance.png"),
    "Puma": img_to_base64("logo_puma.png"),
    "Under Armour": img_to_base64("logo_underarmour.png"),
    "Converse": img_to_base64("logo_converse.png"),
    "Decathlon": img_to_base64("logo_decathlon.png"),
    "Yonex": img_to_base64("logo_yonex.png"),
    "Sperry": img_to_base64("logo_sperry.png"),
}

# =================================================
# CSS (화이트 테마 + 리스트 스크롤)
# =================================================
st.markdown("""
<style>
:root { color-scheme: light !important; }

body, .stApp {
    background-color: white !important;
    color: black !important;
}

.brand-box {
    display: flex;
    align-items: center;
    gap: 6px;
}

.factory-list {
    background: #111;
    color: white;
    padding: 12px;
    border-radius: 10px;
    height: 700px;
    overflow-y: auto;
}

.factory-list button {
    width: 100%;
    text-align: left;
    color: white !important;
    background: #1f1f1f;
    border: 1px solid #333;
    margin-bottom: 6px;
}

.factory-list button:hover {
    background: #333;
}
</style>
""", unsafe_allow_html=True)

# =================================================
# Ducksan
# =================================================
DUCKSAN = {
    "name": "Ducksan Factory",
    "lat": -6.385298062386163,
    "lon": 107.24043447439371,
}

# =================================================
# 공장 데이터 (36개 전부)
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
    (11,"Nike","SCI Selalu Cinta",-7.3649526370117275,110.50302727705107,"317 min (442km)"),
    (12,"Nike","RY.JJS Changshin",-7.074890966054376,108.07273203695073,"160 min (152km)"),
    (13,"Nike","RY Pou Yuen",-6.803464029220425,107.22441150566885,"128 min (72km)"),
    (14,"Nike","JX Pratama",-6.86320705203383,107.02668764100862,"173 min (90km)"),

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
    (26,"Adidas","PGD.PGD2 Glostar Newbal, Adidas",-6.974318300905597,106.83196261494169,"153 min (138km)"),

    (27,"New Balance","PWI-2 Parkland",-6.164065615736655,106.34362393191581,"127 min (134km)"),
    (28,"New Balance","MPI Metro Pearl",-6.553123695397186,107.43167326062274,"57 min (51km)"),

    (30,"Puma","IDM Diamond",-6.760451512559341,108.26909332164612,"124 min (151km)"),
    (31,"Under Armour","Dean Shoes",-6.391000160605475,107.39562888401743,"43 min (29km)"),
    (32,"Under Armour","Long Rich",-6.8755937402321985,108.775905329925,"150 min (200km)"),
    (33,"Converse","SJI Shoenary",-7.369617174917486,110.22038960678333,"350 min (460km)"),
    (34,"Decathlon","DPS-2 Dwi Prima",-7.398359508521098,111.50982327782442,"398 min (567km)"),
    (35,"Yonex","DPS Dwi Prima",-7.505210694143256,111.65093697468592,"405 min (591km)"),
    (36,"Sperry","WWW Young Tree",-7.565685915234356,110.76484773866882,"360 min (482km)")
]

# =================================================
# 헤더
# =================================================
st.markdown(
    f"""
    <div style="display:flex;align-items:center;gap:16px;">
        <img src="data:image/png;base64,{COMPANY_LOGO}" height="60">
        <h1>Factory Distance Map</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# =================================================
# 브랜드 선택 (로고 + 체크박스)
# =================================================
brands = sorted(set([f[1] for f in factories]))
brand_flags = {}

cols = st.columns(len(brands))
for i, b in enumerate(brands):
    with cols[i]:
        st.markdown(
            f"""
            <div class="brand-box">
                <img src="data:image/png;base64,{BRAND_LOGOS[b]}" height="28">
            </div>
            """,
            unsafe_allow_html=True
        )
        brand_flags[b] = st.checkbox(b, True)

visible = [f for f in factories if brand_flags[f[1]]]

# =================================================
# 레이아웃
# =================================================
col_map, col_list = st.columns([4,1])

# =================================================
# 지도
# =================================================
with col_map:
    m = folium.Map(location=[-6.6,108.2], zoom_start=7)

    folium.CircleMarker(
        [DUCKSAN["lat"], DUCKSAN["lon"]],
        radius=8,
        color="blue",
        fill=True,
        fill_color="blue"
    ).add_to(m)

    targets = [st.session_state["selected_factory"]] if st.session_state["selected_factory"] else visible

    for f in targets:
        folium.Marker([f[3], f[4]], popup=f"{f[2]}<br>{f[5]}").add_to(m)

    if st.session_state["selected_factory"]:
        f = st.session_state["selected_factory"]
        dist = haversine_km(DUCKSAN["lat"], DUCKSAN["lon"], f[3], f[4])
        logo = BRAND_LOGOS[f[1]]

        folium.PolyLine(
            [[DUCKSAN["lat"], DUCKSAN["lon"]],[f[3], f[4]]],
            color="black", weight=4
        ).add_to(m)

        m.get_root().html.add_child(Element(f"""
        <div style="position:fixed;top:20px;right:20px;
        background:white;padding:14px;border-radius:10px;
        box-shadow:0 4px 12px rgba(0,0,0,0.15);z-index:9999;">
            <img src="data:image/png;base64,{logo}" height="40"><br><br>
            <b>{f[2]}</b><br>
            브랜드: {f[1]}<br>
            거리: {dist:.1f} km<br>
            소요시간: {f[5]}
        </div>
        """))

    st_folium(m, height=700, width=1400)

# =================================================
# 공장 리스트
# =================================================
with col_list:
    st.markdown('<div class="factory-list">', unsafe_allow_html=True)
    if st.button("전체 공장 보기"):
        st.session_state["selected_factory"] = None

    for f in visible:
        if st.button(f"{f[1]} | {f[2]}", key=f"btn_{f[0]}"):
            st.session_state["selected_factory"] = f

    st.markdown("</div>", unsafe_allow_html=True)
