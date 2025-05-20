class Customer:
    def __init__(self, customer_id, boarding_stop, getoff_stop, time):
        self.customer_id = customer_id
        self.boarding_stop = boarding_stop
        self.getoff_stop = getoff_stop
        self.time = time  # 고객이 정류장에서 대기하기 시작하는 시간


'''
class Customer:
    def __init__(self, customer_id, boarding_stop, getoff_stop, time):
        self.customer_id = customer_id
        self.boarding_stop = boarding_stop
        self.getoff_stop = getoff_stop
        self.time = time

    def __repr__(self):
        return f"Customer({self.customer_id}, {self.boarding_stop}, {self.getoff_stop}, {self.time})"
'''