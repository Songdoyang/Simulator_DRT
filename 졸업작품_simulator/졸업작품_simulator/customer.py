class Customer:
    def __init__(self, customer_id, age, boarding_stop, getoff_stop, time):
        self.customer_id = customer_id
        self.age = age
        self.boarding_stop = boarding_stop
        self.getoff_stop = getoff_stop
        self.time = time

    def __repr__(self):
        return f"Customer({self.customer_id}, {self.age}, {self.boarding_stop}, {self.getoff_stop}, {self.time})"