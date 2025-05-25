import matplotlib.pyplot as plt
# 실패작임
# 매핑하기
stop_coords = {
    '00_오이도차고지': (1, 1),
    '04_오이도종합어시장': (2, 1),
    '05_함상전망대': (3, 1),
    '21_이마트': (4, 2),
    '25_정왕역환승센터': (5, 3),
    '11_열병합발전소': (6, 2),
    '12_우진플라스코': (7, 2),
    '14_우석철강': (8, 2),
    '15_파워맥스': (9, 3),
    '17_홈플러스': (10, 4),
    '24_정왕역': (11, 4),
    '28_시화정형외과': (12, 5),
    '29_금강아파트': (13, 5),
    '30_이마트': (14, 6),
    '31_중앙도서관': (15, 6),
    '34_홈플러스': (16, 6),
    '46_함상전망대': (17, 7),
    '40_열병합발전소': (18, 8),
    '50_오이도차고지': (19, 1),
}

# GA결과 리스트
ga_routes = [
    ['04_오이도종합어시장', '05_함상전망대', '21_이마트', '25_정왕역환승센터', '00_오이도차고지'],
    ['11_열병합발전소', '12_우진플라스코', '14_우석철강', '15_파워맥스', '17_홈플러스',
     '24_정왕역', '25_정왕역환승센터', '28_시화정형외과', '29_금강아파트', '30_이마트',
     '31_중앙도서관', '34_홈플러스', '50_오이도차고지', '46_함상전망대', '40_열병합발전소',
     '00_오이도차고지'],
    # ... 더 많은 운행 루트
]

# 3. 시각화 함수 정의
def visualize_route(route_names, route_number):
    route_points = []

    for stop_name in route_names:
        if stop_name in stop_coords:
            x, y = stop_coords[stop_name]
            route_points.append((x, y, stop_name))
        else:
            print(f"[경고] '{stop_name}'에 대한 좌표가 정의되어 있지 않습니다.")

    x = [p[0] for p in route_points]
    y = [p[1] for p in route_points]
    labels = [p[2] for p in route_points]

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o', linestyle='-', color='blue')
    for i in range(len(x)):
        plt.text(x[i], y[i], labels[i], fontsize=9, ha='right')

    plt.title(f'[{route_number}번째 운행 경로]')
    plt.xlabel('X 좌표')
    plt.ylabel('Y 좌표')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# 4. 전체 운행 경로 반복 시각화
for i, route in enumerate(ga_routes, start=1):
    visualize_route(route, i)
