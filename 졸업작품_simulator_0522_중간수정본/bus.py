class Bus:
    def __init__(self, bus_id, current_stop, max_capacity):
        self.bus_id = bus_id
        self.current_stop = current_stop
        self.max_capacity = max_capacity
        self.onboard_customers = []

        self.total_distance = 0.0
        self.total_boarded_customers = 0
        self.start_time = None
        self.end_time = None

        self.next_stop = None
        self.departure_time = None
        self.is_moving = False

    def is_idle(self):
        return not self.is_moving and len(self.onboard_customers) < self.max_capacity

    def start_move(self):
        self.is_moving = True

    def finish_move(self):
        self.is_moving = False

    def can_board_customer(self):
        return len(self.onboard_customers) < self.max_capacity

    def board_customer(self, customer, boarding_time):
        self.onboard_customers.append(customer)
        self.total_boarded_customers += 1
        if self.start_time is None:
            self.start_time = boarding_time

    def drop_customer(self, stop, current_time):
        dropped = [c for c in self.onboard_customers if c.getoff_stop == stop]
        self.onboard_customers = [c for c in self.onboard_customers if c.getoff_stop != stop]
        return dropped

    def move_to_next_stop(self, stop, distance, arrival_time):
        self.current_stop = stop
        self.total_distance += distance
        self.end_time = arrival_time
