import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from simulator import Simulation
from visualization_route import plot_route

def load_data():
    return {
        "25번": pd.read_excel("정류장_좌표.xlsx")
        # 예시: "26번": pd.read_excel("정류장_좌표_26.xlsx")
    }

def run_simulation_for_route(route_key):
    # 노선별로 시뮬레이션 캐싱
    if 'simulations' not in st.session_state:
        st.session_state.simulations = {}
    if route_key not in st.session_state.simulations:
        sim = Simulation()
        st.session_state.simulations[route_key] = sim.run()
    return st.session_state.simulations[route_key]

def main():
    st.title("🚌 노선 및 시간대별 경로 시각화")

    # 1️⃣ 노선 데이터 불러오기
    route_dfs = load_data()
    route_options = ["-- 노선을 선택하세요 --"] + list(route_dfs.keys())

    # 2️⃣ 노선 선택
    selected_route = st.selectbox("노선을 선택하세요", options=route_options)

    # 3️⃣ 노선이 선택되었을 때만 실행
    if selected_route != "-- 노선을 선택하세요 --":
        # 시뮬 실행
        total_route = run_simulation_for_route(selected_route)

        # 시간대 선택
        selected_hour = st.selectbox("시간대를 선택하세요", options=sorted(total_route.keys()))

        # 해당 시간대의 정류장 좌표 매핑
        df_selected = route_dfs[selected_route]
        plot_df = pd.DataFrame()
        for station in total_route[selected_hour]: 
            station_id = station.split('(')[0]
            plot_df = pd.concat([plot_df, df_selected[df_selected['정류장_ID'] == station_id]], axis=0)

        # 지도 시각화
        m = plot_route(plot_df)
        st.subheader("🗺️ 경로 지도")
        st_folium(m, width=700, height=500)
    else:
        st.info("노선을 선택해주세요.")

if __name__ == "__main__":
    main()
