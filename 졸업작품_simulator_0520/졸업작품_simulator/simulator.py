import heapq
from customer import Customer
from bus import Bus
from utils import get_distance_between, calculate_cost
from parameters import load_fixed_customers


class Event:
    def __init__(self, time, customer=None, bus=None, event_type="boarding"):
        self.time = time
        self.customer = customer
        self.bus = bus
        self.event_type = event_type

    def __lt__(self, other):
        return self.time < other.time


class Simulation:
    def __init__(self):
        self.events = []
        self.customers = []
        self.buses = []
        self.waiting_customers = {}
        self.current_time = 0

    def generate_customers(self):
        fixed_customers = load_fixed_customers()
        for customer in fixed_customers:
            self.customers.append(customer)
            if customer.boarding_stop not in self.waiting_customers:
                self.waiting_customers[customer.boarding_stop] = []
            self.waiting_customers[customer.boarding_stop].append(customer)
            self.schedule_event(customer)

    def schedule_event(self, customer):
        event = Event(customer.time, customer=customer, event_type="boarding")
        heapq.heappush(self.events, event)

    def schedule_bus_move(self, bus, from_stop, to_stop, start_time):
        distance = get_distance_between(from_stop, to_stop)
        if distance is None:
            return

        travel_time = int(distance * 3)
        arrival_time = start_time + travel_time
        event = Event(time=arrival_time, bus=bus, event_type="bus_move")
        heapq.heappush(self.events, event)

        print(f"[{start_time}분 → {arrival_time}분] {bus.bus_id} 이동 예약: {from_stop} → {to_stop} ({distance}km)")
        bus.next_stop = to_stop
        bus.departure_time = start_time
        bus.start_move()

    def handle_event(self, event):
        if event.event_type == "boarding":
            stop = event.customer.boarding_stop
            bus = self.get_bus_at_stop(stop)
            if bus and bus.can_board_customer() and event.customer.time <= self.current_time:
                bus.board_customer(event.customer, self.current_time)
                print(f"[{self.current_time}분] {event.customer.customer_id}번 고객이 {bus.bus_id} 버스에 탑승")
                self.waiting_customers[stop].remove(event.customer)

                # 목적지로 이동 예약
                bus.start_move()
                self.schedule_bus_move(bus, bus.current_stop, event.customer.getoff_stop, self.current_time)

        elif event.event_type == "bus_move":
            bus = event.bus
            distance = get_distance_between(bus.current_stop, bus.next_stop)
            if distance is not None:
                bus.move_to_next_stop(bus.next_stop, distance, event.time)
                bus.finish_move()
                print(f"[{event.time}분] {bus.bus_id} 버스가 {bus.next_stop}에 도착")

                # 하차 처리
                dropped = bus.drop_customer(bus.current_stop, event.time)
                for c in dropped:
                    print(f"[{event.time}분] {c.customer_id}번 고객이 {bus.bus_id} 버스에서 하차")

                # 도착한 곳에 대기 고객 있으면 이벤트 재등록
                stop = bus.current_stop
                if stop in self.waiting_customers:
                    for c in list(self.waiting_customers[stop]):
                        if c.time <= self.current_time:
                            self.schedule_event(c)

    def get_bus_at_stop(self, stop):
        for bus in self.buses:
            if bus.current_stop == stop and not bus.is_moving:
                return bus
        return None

    def run(self):
        self.generate_customers()

        while self.events:
            event = heapq.heappop(self.events)
            self.current_time = event.time
            self.handle_event(event)

        self.end_simulation()

    def end_simulation(self):
        self.print_summary()

    def print_summary(self):
        print("\n시뮬레이션 결과 요약")
        total_distance = 0.0
        total_customers = 0
        total_cost = 0.0

        for bus in self.buses:
            duration = (bus.end_time - bus.start_time) if bus.start_time is not None and bus.end_time is not None else 0
            print(f"{bus.bus_id} 이동거리: {bus.total_distance:.2f} km | 탑승 고객: {bus.total_boarded_customers}명 | "
                  f"운영비: {calculate_cost(bus.total_distance):.0f}원 | 운행 시간: {duration}분")
            total_distance += bus.total_distance
            total_customers += bus.total_boarded_customers
            total_cost += calculate_cost(bus.total_distance)

        print(f"\n총 이동거리: {total_distance:.2f} km")
        print(f"총 탑승 고객 수: {total_customers}명")
        print(f"총 운영비: {total_cost:.0f}원")


# 실행
if __name__ == "__main__":
    sim = Simulation()
    sim.buses.append(Bus(bus_id="Bus1", current_stop="A", max_capacity=5))
    sim.buses.append(Bus(bus_id="Bus2", current_stop="A", max_capacity=5))
    sim.buses.append(Bus(bus_id="Bus3", current_stop="A", max_capacity=5))
    sim.run()
