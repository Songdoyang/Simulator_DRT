
# utils.py

# 운영비 계산 (1km당 100원)
def calculate_cost(distance):
    return distance * 100

# (필요 시 경로 최적화용 함수)
def get_shortest_route(customers):
    stops = set()
    for c in customers:
        stops.add(c.boarding_stop)
        stops.add(c.getoff_stop)
    return sorted(list(stops))
'''
# 거리 정보 (대칭, A→B와 B→A는 같은 거리로 처리)
distance_map = {
    ('A', 'B'): 2.3,
    ('B', 'C'): 1.2,
    ('A', 'C'): 3.1
}

# 운영비 계산 (1km당 100원)
def calculate_cost(distance):
    return distance * 100

# 정류장 간 거리 조회 함수
def get_distance_between(stop_a, stop_b):
    return distance_map.get((stop_a, stop_b)) or distance_map.get((stop_b, stop_a))

# (사용 안 할 경우 생략 가능)
def get_shortest_route(customers):
    stops = set()
    for c in customers:
        stops.add(c.boarding_stop)
        stops.add(c.getoff_stop)
    return sorted(list(stops))
'''