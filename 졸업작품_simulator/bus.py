from utils import get_distance_between

class Bus:
    def __init__(self, bus_id, max_capacity=15):
        self.bus_id = bus_id
        self.current_stop = None
        self.onboard_customers = []  # 현재 승객
        self.route = []  # 경로
        self.finished_customers = []  # 하차한 고객들
        self.total_distance = 0  # 총 이동 거리
        self.passed_stops = set()  # 지나간 정류장
        self.max_capacity = max_capacity  # 최대 수용 인원

    def board_customer(self, customer):
        if len(self.onboard_customers) < self.max_capacity:
            self.onboard_customers.append(customer)
            print(f"Customer {customer.customer_id} boarded on Bus {self.bus_id}")
        else:
            print(f"Bus {self.bus_id} is full, cannot board Customer {customer.customer_id}")

    def drop_customer(self, stop_id, current_time):
        dropping = [c for c in self.onboard_customers if c.getoff_stop == stop_id]
        self.onboard_customers = [c for c in self.onboard_customers if c.getoff_stop != stop_id]
        self.finished_customers.extend([(c, current_time) for c in dropping])
        return dropping

    def move_to_next_stop(self, next_stop, distance):
        self.total_distance += distance 
        self.current_stop = next_stop
        self.passed_stops.add(next_stop)

    def is_idle(self):
        return len(self.onboard_customers) == 0

    def get_total_distance(self):
        return self.total_distance

    def get_closest_stop(self, potential_stops):
        closest_stop = None
        min_distance = float('inf')

        for stop in potential_stops:
            if stop in self.passed_stops:
                continue  # 지나간 정류장은 제외

            distance = get_distance_between(self.current_stop, stop)
            if distance < min_distance:
                closest_stop = stop
                min_distance = distance

        return closest_stop

    def can_board_customer(self):
        return len(self.onboard_customers) < self.max_capacity
