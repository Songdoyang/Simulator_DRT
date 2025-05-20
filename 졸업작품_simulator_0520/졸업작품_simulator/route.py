def get_distance_between(stop1, stop2):
    # 간단한 예시용 거리 계산
    if stop1 == stop2:
        return 0
    return 5  # 고정 거리
'''
from utils import get_distance_between

def update_route(bus, waiting_customers):
    potential_stops = set(waiting_customers.keys())
    for customer in bus.onboard_customers:
        potential_stops.add(customer.getoff_stop)

    next_stop = bus.get_closest_stop(potential_stops)
    if next_stop:
        distance = get_distance_between(bus.current_stop, next_stop)
        bus.move_to_next_stop(next_stop, distance)
        print(f"{bus.bus_id}버스가 {next_stop}으로 이동합니다. (이동거리리: {distance} km)")
    else:
        print(f"{bus.bus_id}버스가 운행을 종료합니다.")
'''