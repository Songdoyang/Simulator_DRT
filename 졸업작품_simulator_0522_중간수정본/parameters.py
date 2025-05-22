from customer import Customer

# 고정된 고객 목록을 반환
def load_fixed_customers():
    return [
        Customer(0, "07_대부도입구구", "08_시화환경사업소", 9),
        Customer(1, "01_삼양사", "47_오이도종합어시장", 10),
        Customer(2, "08_시화환경사업소", "14_우석철강", 11),
        Customer(3, "06_오이도박물관", "25_정왕역환승센터", 13),
        Customer(4, "17_홈플러스", "19_계룡1차아파트", 11),
        Customer(5, "43_시화환경사업소", "47_오이도종합어시장", 9)
    ]
'''
from customer import Customer

# 고정된 고객 목록을 반환
def load_fixed_customers():
    return [
        Customer(0, "A", "B", 9),
        Customer(1, "A", "C", 10),
        Customer(2, "B", "A", 11),
        Customer(3, "C", "A", 13),
        Customer(4, "B", "C", 11),
        Customer(5, "A", "B", 9)
    ]

# 필요 시 추후 확률 기반 생성도 가능
# def generate_customers_from_distribution():
#     ...............................................
통계기반으로 랜덤하게 만들기 고정아님
from customer import Customer

def generate_customers_from_distribution(num_customers=100):
    np.random.seed(42)  # 재현 가능성
    stops = ["A", "B", "C"]
    customers = []

    for i in range(num_customers):
        start = np.random.choice(stops)
        end = np.random.choice([s for s in stops if s != start])
        time = int(np.random.normal(loc=12, scale=2))
        time = max(0, min(23, time))  # 0~23시 사이 제한
        customers.append(Customer(i, start, end, time))

    return customers

'''
