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

# =================================================
# 🔴 우리 공장 (고정)
# =================================================
OUR_FACTORY = (
    "OUR",
    "Our Factory",
    -6.200000,   # 위도
    106.800000   # 경도
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
    <div style="display:flex;align-items:center;gap:20px;margin-bottom:20px;">
        <img src="data:image/png;base64,{company_logo}" height="60">
        <h1 style="margin:0;">Factory Distance Map</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# =================================================
# 브랜드 선택 + 전체 선택/해제
# =================================================
st.markdown("### 브랜드 선택")

b1, b2, _ = st.columns([1,1,6])

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

for i, (brand, logo) in enumerate(brand_logos.items()):
    with cols[i % 5]:
        st.image(logo, width=70)
        brand_checks[brand] = st.checkbox(
            brand,
            key=f"brand_{brand}",
            value=st.session_state.get(f"brand_{brand}", True)
        )

# =================================================
# 공장 데이터
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
    (33,"Converse","SJI Shoenary",-7.369617174917486,110.22038960678333,"350 min (460km)")
]

visible_factories = [f for f in factories if brand_checks.get(f[1], False)]

# =================================================
# 메인 레이아웃
# =================================================
col_map, col_list = st.columns([4,1])

# ================= 지도 =================
with col_map:
    sf = st.session_state["selected_factory"]

    # 지도 위 정보 (선택 시)
    if sf:
        st.info(
            f"""
            **선택 공장**
            - 브랜드 : {sf[1]}
            - 공장명 : {sf[2]}
            - 소요시간 : {sf[5]}
            """
        )

    m = folium.Map(location=[-6.6,108.2], zoom_start=7)

    # 🔵 우리 공장 마커
    folium.Marker(
        [OUR_FACTORY[2], OUR_FACTORY[3]],
        popup=OUR_FACTORY[1],
        icon=folium.Icon(color="green", icon="home")
    ).add_to(m)

    # 일반 공장 마커
    for f in visible_factories:
        folium.Marker([f[3], f[4]], popup=f[2]).add_to(m)

    # 🔴 선택 공장 + 우리 공장 연결선 (단 하나)
    if sf:
        folium.Marker(
            [sf[3], sf[4]],
            icon=folium.Icon(color="red", icon="star"),
            popup=sf[2]
        ).add_to(m)

        folium.PolyLine(
            [[OUR_FACTORY[2], OUR_FACTORY[3]], [sf[3], sf[4]]],
            color="blue",
            weight=3
        ).add_to(m)

    st_folium(m, height=700, width=1400)

# ================= 공장 리스트 =================
with col_list:
    st.markdown("### 공장 리스트")
    with st.container(height=700):
        for f in visible_factories:
            if st.button(f"{f[1]} | {f[2]}", key=f"factory_{f[0]}"):
                st.session_state["selected_factory"] = f
