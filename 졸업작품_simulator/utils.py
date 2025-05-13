distance_map = {
    ('A', 'B'): 2.3,
    ('B', 'C'): 1.2,
    ('A', 'C'): 3.1
}

agecost_table = {
    "child": 450,
    "teen": 720,
    "adult": 1250,
    "senior": 0
}

def calculate_fare(age):
    if age <= 12:
        return agecost_table["child"]
    elif age <= 19:
        return agecost_table["teen"]
    elif age <= 60:
        return agecost_table["adult"]
    else:
        return agecost_table["senior"]

def calculate_cost(distance):
    return distance * 100  # 예시: 1 km 당 100원의 비용

def get_distance_between(stop_a, stop_b):
    return distance_map.get((stop_a, stop_b)) or distance_map.get((stop_b, stop_a))

def get_shortest_route(customers):
    # 고객들이 탑승하는 경로를 생성하는 함수
    stops = set()
    for c in customers:
        stops.add(c.boarding_stop)
        stops.add(c.getoff_stop)
    return sorted(list(stops))
