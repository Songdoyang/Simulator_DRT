from parameters import load_fixed_customers
from customer import Customer
from utils import get_distance_between, calculate_cost
from bus import Bus
from ga_optimizer import run_ga
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import pandas as pd

try:
    from adjustText import adjust_text
    ADJUST_TEXT_AVAILABLE = True
except ImportError:
    print("경고: adjustText 모듈이 설치되어 있지 않습니다. 텍스트 자동 조정이 작동하지 않습니다.")
    ADJUST_TEXT_AVAILABLE = False

def set_korean_font():
    if platform.system() == 'Windows':
        font_path = "C:/Windows/Fonts/malgun.ttf"
    elif platform.system() == 'Darwin':
        font_path = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"
    else:
        font_path = None

    if font_path:
        fontprop = fm.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = fontprop.get_name()
    else:
        print("한글 폰트를 찾을 수 없습니다. 한글 출력이 깨질 수 있습니다.")

set_korean_font()

class Simulation:
    def __init__(self):
        self.customers = []
        self.buses = []
        self.waiting_customers = {}  # {정류장: [대기중 고객 리스트]}
        self.current_time = 600  # 10시 00분 (분 단위)
        self.bus_counter = 1

    def generate_customers(self):
        fixed_customers = load_fixed_customers()
        for c in fixed_customers:
            if c.boarding_stop != c.getoff_stop:
                self.customers.append(c)
                self.waiting_customers.setdefault(c.boarding_stop, []).append(c)

    def run(self):
        self.generate_customers()

        # 첫 번째 버스 투입
        self.buses.append(Bus(bus_id="Bus1", current_stop="00_오이도차고지", max_capacity=30))
        print("[시작] 10시부터 16시까지 시뮬레이션 시작")

        for hour in range(10, 17):
            print(f"\n[{hour}시 ~ {hour+1}시 구간 운행]")
            hour_min = hour * 60

            # 해당 시간대 고객 필터링
            hourly_customers = [c for c in self.customers if hour_min <= c.time < hour_min + 60]
            hourly_customer_ids = {c.customer_id for c in hourly_customers}
            remaining_customers = hourly_customers.copy()

            # GA로 최적 정류장 순서 찾기
            stops_to_visit = self.get_stops_in_order(hourly_customers)
            print(f"운행 경로: {stops_to_visit}")

            bus_index = 0
            while remaining_customers:
                if bus_index >= len(self.buses):
                    self.bus_counter += 1
                    new_bus = Bus(bus_id=f"Bus{self.bus_counter}", current_stop="00_오이도차고지", max_capacity=30)
                    self.buses.append(new_bus)

                bus = self.buses[bus_index]
                bus_index += 1

                unfinished_ids = {c.customer_id for c in remaining_customers}
                while unfinished_ids:
                    for i, stop in enumerate(stops_to_visit):
                        if i > 0:
                            prev_stop = stops_to_visit[i-1]
                            dist = get_distance_between(prev_stop, stop)
                            if dist is not None:
                                bus.total_distance += dist
                                self.current_time += int(dist * 3)

                        bus.update_stop(stop)

                        # 하차 처리
                        dropped_customers = bus.drop_customer(stop, self.current_time)
                        for c in dropped_customers:
                            c.dropoff_time = self.current_time
                            h, m = divmod(self.current_time, 60)
                            print(f"[{h:02d}:{m:02d}] 고객 {c.customer_id} 하차 (버스: {bus.bus_id}, 정류장: {stop})")

                        # 탑승 처리
                        waiting_list = list(self.waiting_customers.get(stop, []))
                        for c in waiting_list:
                            if c.customer_id in hourly_customer_ids and c.time <= self.current_time and bus.can_board_customer():
                                bus.board_customer(c, self.current_time)
                                self.waiting_customers[stop].remove(c)
                                c.pickup_time = self.current_time
                                h, m = divmod(self.current_time, 60)
                                print(f"[{h:02d}:{m:02d}] 고객 {c.customer_id} 탑승 (버스: {bus.bus_id}, 정류장: {stop}, 하차: {c.getoff_stop})")

                    unfinished_ids = {c.customer_id for c in remaining_customers if c.customer_id not in {cust.customer_id for cust, _ in bus.finished_customers}}

                bus.end_time = self.current_time
                remaining_customers = [c for c in remaining_customers if c.customer_id not in {cust.customer_id for cust, _ in bus.finished_customers}]

            # 정류장 복귀 및 시각화 처리
            self.return_buses_to_depot_if_time_allows(hour)

        # 남은 고객 추가 운행 처리
        self.handle_remaining_customers()

        # 시뮬레이션 종료 및 결과 출력
        self.end_simulation()

    def get_stops_in_order(self, customers):
        pairs = [(c.boarding_stop, c.getoff_stop) for c in customers]
        if not pairs:
            return []
        return run_ga(pairs)

    def return_buses_to_depot_if_time_allows(self, hour):
        next_hour = (hour + 1) * 60
        time_gap = next_hour - self.current_time
        if time_gap >= 15:
            for bus in self.buses:
                if bus.current_stop != "00_오이도차고지":
                    dist = get_distance_between(bus.current_stop, "00_오이도차고지")
                    if dist:
                        bus.total_distance += dist
                        self.current_time += int(dist * 3)
                        bus.update_stop("00_오이도차고지")
                        h, m = divmod(self.current_time, 60)
                        print(f"[{h:02d}:{m:02d}] {bus.bus_id} 버스가 오이도차고지로 복귀하여 대기")

            stop_coords = self.load_stop_coordinates("C:/Users/sking/Desktop/졸작/시뮬/25번정류장_좌표.xlsx")
            for bus in self.buses:
                self.plot_route_segments_subplots(bus, stop_coords)

        else:
            h, m = divmod(self.current_time, 60)
            print(f"[{h:02d}:{m:02d}] 버스들이 대기 없이 다음 정류장으로 이동")

    def handle_remaining_customers(self):
        while True:
            remaining_customers = [c for c in self.customers if c.dropoff_time is None]
            if not remaining_customers:
                break

            print("\n[추가 운행] 남은 고객 처리 중...")
            stops_to_visit = self.get_stops_in_order(remaining_customers)

            for bus in self.buses:
                unfinished_ids = {c.customer_id for c in remaining_customers}
                while unfinished_ids:
                    for i, stop in enumerate(stops_to_visit):
                        if i > 0:
                            prev_stop = stops_to_visit[i - 1]
                            dist = get_distance_between(prev_stop, stop)
                            if dist:
                                bus.total_distance += dist
                                self.current_time += int(dist * 3)

                        bus.update_stop(stop)

                        dropped = bus.drop_customer(stop, self.current_time)
                        for c in dropped:
                            c.dropoff_time = self.current_time
                            h, m = divmod(self.current_time, 60)
                            print(f"[{h:02d}:{m:02d}] 고객 {c.customer_id} 하차 (버스: {bus.bus_id}, 정류장: {stop})")

                    unfinished_ids = {c.customer_id for c in remaining_customers if c.customer_id not in {cust.customer_id for cust, _ in bus.finished_customers}}

                bus.end_time = self.current_time

            stop_coords = self.load_stop_coordinates("C:/Users/sking/Desktop/졸작/시뮬/25번정류장_좌표.xlsx")
            for bus in self.buses:
                self.plot_route_segments_subplots(bus, stop_coords)


    def end_simulation(self):
        print("\n=== 시뮬레이션 종료 ===")
        self.print_summary()

    def print_summary(self):
        print("\n시뮬레이션 결과 요약")
        total_distance = 0.0
        total_customers = 0
        total_cost = 0.0

        for bus in self.buses:
            if bus.total_boarded_customers == 0:
                print(f"{bus.bus_id}은(는) 운행하지 않았습니다.")
            else:
                duration = (bus.end_time - bus.start_time) if bus.end_time and bus.start_time else 0
                cost = calculate_cost(bus.total_distance)
                print(f"{bus.bus_id} 이동거리: {bus.total_distance:.2f} km | 고객 수: {bus.total_boarded_customers}명 | 운영비: {cost:.0f}원 | 운행 시간: {duration}분")
                total_distance += bus.total_distance
                total_customers += bus.total_boarded_customers
                total_cost += cost

        print(f"\n총 이동거리: {total_distance:.2f} km")
        print(f"총 고객 수: {total_customers}명")
        print(f"총 운영비: {total_cost:.0f}원")

    def load_stop_coordinates(self, filepath):
        df = pd.read_excel(filepath)
        stop_coords = {}
        for _, row in df.iterrows():
            stop_coords[row['정류장_ID']] = (row['y'], row['x'])
        return stop_coords

    def plot_ga_routes_for_buses(self, buses, stop_coords):
        for bus in buses:
            if len(bus.visited_stops) > 1:
                print(f"--- {bus.bus_id} 경로 시각화 ---")
                self.plot_route_segments(bus, stop_coords)
    #이게 시각화임
    def plot_route_segments_subplots(self, bus, stop_coords):
        import math

        # 폰트 설정
        if platform.system() == 'Windows':
            font_path = "C:/Windows/Fonts/malgun.ttf"
        elif platform.system() == 'Darwin':
            font_path = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"
        else:
            font_path = None
        fontprop = fm.FontProperties(fname=font_path) if font_path else None

        base_stop = "00_오이도차고지"
        visited = bus.visited_stops

        base_indices = [i for i, stop in enumerate(visited) if stop == base_stop]
        if not base_indices or base_indices[-1] != len(visited) - 1:
            base_indices.append(len(visited) - 1)

        segments = []
        start_idx = 0
        for end_idx in base_indices:
            segment_stops = visited[start_idx:end_idx+1]
            if len(segment_stops) >= 2:
                segments.append((start_idx, end_idx, segment_stops))
            start_idx = end_idx + 1

        n = len(segments)
        if n == 0:
            print("그릴 구간이 없습니다.")
            return

        cols = 3
        rows = math.ceil(n / cols)

        fig, axs = plt.subplots(rows, cols, figsize=(cols * 6, rows * 5))
        axs = axs.flatten() if n > 1 else [axs]

        for i, (start_idx, end_idx, segment_stops) in enumerate(segments):
            lats, lons = [], []
            for stop in segment_stops:
                if stop in stop_coords:
                    lat, lon = stop_coords[stop]
                    lats.append(lat)
                    lons.append(lon)

            ax = axs[i]
            ax.plot(lons, lats, marker='o', color='blue', linewidth=2)

            texts = []
            for stop, x, y in zip(segment_stops, lons, lats):
                t = ax.text(x, y, stop, fontsize=8, verticalalignment='bottom', horizontalalignment='right', fontproperties=fontprop)
                texts.append(t)

            if ADJUST_TEXT_AVAILABLE:
                adjust_text(texts, ax=ax, only_move={'points':'y', 'texts':'y'}, arrowprops=dict(arrowstyle='->', color='red', lw=0.5))

            ax.set_title(f'버스 경로 구간 {start_idx}~{end_idx}')
            ax.set_xlabel('경도')
            ax.set_ylabel('위도')
            ax.grid(True)

        for j in range(i + 1, len(axs)):
            fig.delaxes(axs[j])

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    sim = Simulation()
    sim.run()