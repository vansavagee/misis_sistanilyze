import math
from collections import Counter

def calculate_entropy(probabilities):
    """Вычисляет энтропию на основе вероятностей."""
    return -sum(p * math.log2(p) for p in probabilities if p > 0)

def calculate_joint_entropy(joint_distribution):
    """Вычисляет совместную энтропию."""
    total = sum(joint_distribution.values())
    probabilities = [count / total for count in joint_distribution.values()]
    return calculate_entropy(probabilities)

def calculate_marginal_distribution(joint_distribution, axis):
    """Вычисляет маргинальное распределение по оси (0 = сумма, 1 = произведение)."""
    marginal = Counter()
    for (sum_val, prod_val), count in joint_distribution.items():
        key = sum_val if axis == 0 else prod_val
        marginal[key] += count
    return marginal

def main():
    # Все возможные результаты броска двух шестигранных костей
    outcomes = [(i, j) for i in range(1, 7) for j in range(1, 7)]
    
    # Вычисляем значения суммы и произведения
    joint_distribution = Counter((i + j, i * j) for i, j in outcomes)

    # Совместная энтропия H(AB)
    H_AB = calculate_joint_entropy(joint_distribution)

    # Маргинальные распределения
    marginal_A = calculate_marginal_distribution(joint_distribution, axis=0)
    marginal_B = calculate_marginal_distribution(joint_distribution, axis=1)

    # Энтропии H(A) и H(B)
    total_outcomes = len(outcomes)
    H_A = calculate_entropy([count / total_outcomes for count in marginal_A.values()])
    H_B = calculate_entropy([count / total_outcomes for count in marginal_B.values()])

    # Условная энтропия H(B|A)
    H_B_A = H_AB - H_A

    # Количество информации I(A, B)
    I_AB = H_B - H_B_A

    # Возврат результата
    return [round(H_AB, 2), round(H_A, 2), round(H_B, 2), round(H_B_A, 2), round(I_AB, 2)]

if __name__ == "__main__":
    print(main())
