import heapq
import random
from datetime import *
from bus import Bus
from route import *
from customer import Customer

class Event:
    def __init__(self, time, customer, event_type):
        self.time = time
        self.customer = customer
        self.event_type = event_type

    def __lt__(self, other):
        return self.time < other.time


class Simulation:
    def __init__(self):
        self.events = []
        self.customers = []
        self.buses = []
        self.waiting_customers = {}
        self.bus_status = {}

    def generate_customers(self):
        for i in range(10):
            customer = Customer(i, random.randint(10, 70), random.choice(["A", "B", "C"]), random.choice(["A", "B", "C"]), random.randint(0, 24))
            self.customers.append(customer)
            if customer.boarding_stop not in self.waiting_customers:
                self.waiting_customers[customer.boarding_stop] = []
            self.waiting_customers[customer.boarding_stop].append(customer)

    def schedule_event(self, customer):
        event = Event(customer.time, customer, "boarding")
        heapq.heappush(self.events, event)

    def handle_event(self, event):
        if event.event_type == "boarding":
            bus = self.get_idle_bus()
            if bus and bus.can_board_customer():
                available_capacity = bus.max_capacity - len(bus.onboard_customers)
                customers_to_board = self.waiting_customers.get(bus.current_stop, [])[:available_capacity]
                for customer in customers_to_board:
                    bus.board_customer(customer)
                    print(f"{customer.customer_id}고객이 {bus.bus_id}버스에 탑승")
                    self.waiting_customers[bus.current_stop].remove(customer)
                for customer in customers_to_board:
                    self.schedule_event(customer)

        elif event.event_type == "dropping":
            bus = self.get_bus_for_customer(event.customer)
            if bus:
                dropped_customers = bus.drop_customer(event.customer.getoff_stop, event.time)
                for dropped_customer in dropped_customers:
                    print(f"{dropped_customer.customer_id}고객이 {bus.bus_id}버스에서 하차")

    def get_idle_bus(self):
        for bus in self.buses:
            if bus.is_idle():
                return bus
        return None

    def get_bus_for_customer(self, customer):
        for bus in self.buses:
            if customer in bus.onboard_customers:
                return bus
        return None

    def update_route(self):
        for bus in self.buses:
            next_stop = bus.get_closest_stop(self.waiting_customers.keys())
            if next_stop:
                distance = get_distance_between(bus.current_stop, next_stop)
                bus.move_to_next_stop(next_stop, distance)
                print(f"{bus.bus_id}버스가 {next_stop}으로 이동 (이동거리: {distance} km)")

    def run(self):
        self.generate_customers()

        while self.events:
            event = heapq.heappop(self.events)
            self.handle_event(event)

        for bus in self.buses:
            self.update_route()

        self.end_simulation()

    def end_simulation(self):
        self.print_summary()

    def print_summary(self):
        print("종료")

simulation = Simulation()
simulation.run()
