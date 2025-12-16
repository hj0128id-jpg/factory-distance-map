import streamlit as st
import folium
from streamlit_folium import st_folium
import base64

# =================================================
# 기본 설정
# =================================================
st.set_page_config(layout="wide", page_title="Factory Distance Map")

if "selected_factory" not in st.session_state:
    st.session_state["selected_factory"] = None

# =================================================
# 유틸
# =================================================
def img_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def select_factory(factory):
    st.session_state["selected_factory"] = factory

def reset_view():
    st.session_state["selected_factory"] = None


# =================================================
# 🔴 우리 공장 (고정 좌표)
# =================================================
OUR_FACTORY = (
    "OUR",
    "Our Factory",
    -6.38528740186252,
    107.24014479421118
)

# =================================================
# 로고
# =================================================
company_logo = img_b64("company_logo.png")

brand_logos = {
    "Nike": "logo_nike.png",
    "Adidas": "logo_adidas.png",
    "New Balance": "logo_newbalance.png",
    "Puma": "logo_puma.png",
    "Converse": "logo_converse.png",
    "Decathlon": "logo_decathlon.png",
    "Under Armour": "logo_underarmour.png",
    "Yonex": "logo_yonex.png",
    "Sperry": "logo_sperry.png",
}

# =================================================
# 헤더
# =================================================
st.markdown(
    f"""
    <div style="margin-bottom:10px;">
        <img src="data:image/png;base64,{company_logo}" height="30">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<h1 style='margin-top:0; margin-bottom:20px;'>Factory Distance Map</h1>",
    unsafe_allow_html=True
)
st.markdown("""
<style>
/* 전체 선택 / 전체 해제 버튼만 작게 보이도록 */
button {
    font-size: 6px !important;
    padding: 4px 10px !important;
}
</style>
""", unsafe_allow_html=True)
# =================================================
# 브랜드 선택 + 전체 선택/해제 (로고 제거 버전)
# =================================================
st.markdown("### 브랜드 선택")

b1, b2, _ = st.columns([2, 2, 28])
with b1:
    if st.button("전체 선택"):
        for b in brand_logos:
            st.session_state[f"brand_{b}"] = True
with b2:
    if st.button("전체 해제"):
        for b in brand_logos:
            st.session_state[f"brand_{b}"] = False

brand_checks = {}
cols = st.columns(5)

for i, brand in enumerate(brand_logos.keys()):
    with cols[i % 5]:
        brand_checks[brand] = st.checkbox(
            brand,
            key=f"brand_{brand}",
            value=st.session_state.get(f"brand_{brand}", True)
        )

# =================================================
# 공장 데이터
# =================================================
factories = [
    (1,"Nike","IY.PIC Nikomas",-6.16276739755951,106.31671924330799,"130 min (135km)"),
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

    (15,"Adidas","PWI-1 Parkland",-6.18005569680193,106.34344218683786,"140 min (131km)"),
    (16,"Adidas","IY.PIC Nikomas",-6.16276739755951,106.31671924330799,"130 min (135km)"),
    (17,"Adidas","PRB Panarub",-6.170607657812733,106.6191471209852,"105 min (107km)"),
    (18,"Adidas","PBB Bintang Indo",-6.867770507966313,108.84263889750521,"167 min (207km)"),
    (19,"Adidas","SHI Tah Sung Hung",-6.929972278573358,108.87605444522376,"167 min (220km)"),
    (20,"Adidas","HWI Hwa Seung",-6.712188897782861,110.72403180338068,"360 min (455km)"),
    (21,"Adidas","PWI-3 Parkland",-6.867770507966313,108.84263889750521,"312 min (416km)"),
    (22,"Adidas","PWI-4 Parkland",-6.7142319309820175,111.38549046857136,"362 min (458km)"),
    (23,"Adidas","HWI-2 Hwa Seung",-6.712771739449992,111.19681124717319,"420 min (500km)"),
    (24,"Adidas","PWi-5 Parkland",-6.709008772441859,111.39741373178808,"447 min (522km)"),
    (25,"Adidas","PGS Pouchen",-6.875398775012465,107.02241821336372,"180 min (93km)"),
    (26,"Adidas","PGD Glostar",-6.974318300905597,106.83196261494169,"153 min (138km)"),

    (27,"New Balance","PWI-2 Parkland",-6.164065615736655,106.34362393191581,"127 min (134km)"),
    (28,"New Balance","MPI Metro Pearl",-6.553123695397186,107.43167326062274,"57 min (51km)"),
    (29,"New Balance","PGD2 Glostar",-6.974318300905597,106.83196261494169,"153 min (138km)"),

    (30,"Puma","IDM Diamond",-6.760451512559341,108.26909332164612,"124 min (151km)"),
    (31,"Under Armour","Dean Shoes",-6.391000160605475,107.39562888401743,"43 min (29km)"),
    (32,"Under Armour","Long Rich",-6.8755937402321985,108.775905329925,"150 min (200km)"),
    (33,"Converse","SJI Shoenary",-7.369617174917486,110.22038960678333,"350 min (460km)"),
    (34,"Decathlon","DPS-2 Dwi Prima",-7.398359508521098,111.50982327782442,"398 min (567km)"),
    (35,"Yonex","DPS Dwi Prima",-7.505210694143256,111.65093697468592,"405 min (591km)"),
    (36,"Sperry","WWW Young Tree",-7.565685915234356,110.76484773866882,"360 min (482km)")
]

visible_factories = [f for f in factories if brand_checks.get(f[1], False)]

# =================================================
# 메인 레이아웃
# =================================================
col_map, col_list = st.columns([4,1])

# ================= 지도 =================
with col_map:
    sf = st.session_state["selected_factory"]

    if sf:
        logo_b64 = img_b64(brand_logos[sf[1]])
        st.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:14px;
                        padding:10px;border:1px solid #ddd;border-radius:8px;
                        margin-bottom:10px;">
                <img src="data:image/png;base64,{logo_b64}" width="60">
                <div>
                    <b>브랜드</b> : {sf[1]}<br>
                    <b>공장명</b> : {sf[2]}<br>
                    <b>소요시간</b> : {sf[5]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    m = folium.Map(location=[-6.6,108.2], zoom_start=7)

    folium.Marker(
        [OUR_FACTORY[2], OUR_FACTORY[3]],
        popup=OUR_FACTORY[1],
        icon=folium.Icon(color="green", icon="home")
    ).add_to(m)

    if sf:
        folium.Marker(
            [sf[3], sf[4]],
            icon=folium.Icon(color="red", icon="star"),
            popup=sf[2]
        ).add_to(m)
    else:
        for f in visible_factories:
            folium.Marker([f[3], f[4]], popup=f[2]).add_to(m)

    st_folium(m, height=600, width=1400)

# ================= 공장 리스트 =================
with col_list:
    h1, h2 = st.columns([3,1])

    with h1:
        st.markdown("### 공장 리스트")

    with h2:
        st.button(
    "🔄",
    help="전체 공장 다시 보기",
    on_click=reset_view
)


    with st.container(height=500):
        for f in visible_factories:
            st.button(
                f"{f[1]} | {f[2]}",
                key=f"factory_{f[0]}",
                on_click=select_factory,
                args=(f,)
            )


# 스크롤 항상 맨 위
st.markdown(
    "<script>window.scrollTo(0, 0);</script>",
    unsafe_allow_html=True
)
