import json

def calculate_membership(value, points):
    """
    Вычисляет степень принадлежности значения value к функции принадлежности, заданной точками points.
    Аргументы:
    - value: текущее значение для вычисления степени принадлежности
    - points: список пар [x, y], описывающих функцию принадлежности
    
    Возвращает:
    - степень принадлежности (от 0 до 1)
    """
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        
        if x1 <= value <= x2:  # проверяем, попадает ли value в интервал [x1, x2]
            if x1 == x2:  # если x1 и x2 совпадают (защита от деления на 0)
                return max(y1, y2)
            # Линейная интерполяция между двумя точками
            return y1 + (y2 - y1) * (value - x1) / (x2 - x1)
    
    return 0  # если значение не попало ни в один из интервалов

def fuzzification(value, membership_functions):
    """
    Выполняет фаззификацию значения value, вычисляя степени принадлежности к каждому терму.
    
    Аргументы:
    - value: текущее значение переменной
    - membership_functions: словарь термов и их функций принадлежности
    
    Возвращает:
    - словарь степеней принадлежности к каждому терму
    """
    fuzzy_values = {}
    for term, points in membership_functions.items():
        fuzzy_values[term] = calculate_membership(value, points)
    return fuzzy_values

def apply_rule(fuzzy_temperature, rules, heating_membership_functions):
    """
    Применяет правила управления для определения выходных степеней принадлежности.
    
    Аргументы:
    - fuzzy_temperature: степени принадлежности текущей температуры к термам (результат фаззификации)
    - rules: словарь логических правил нечеткого управления (например, {"холодно": "интенсивно"})
    - heating_membership_functions: функции принадлежности термов для "уровня нагрева"
    
    Возвращает:
    - степени принадлежности для уровня нагрева
    """
    heating_values = {term: 0 for term in heating_membership_functions.keys()}
    
    for temp_term, heating_term in rules.items():
        if temp_term in fuzzy_temperature and heating_term in heating_values:
            membership_value = fuzzy_temperature[temp_term]
            heating_values[heating_term] = max(heating_values[heating_term], membership_value)  
    
    return heating_values

def defuzzification(heating_values, heating_membership_functions):
    """
    Выполняет дефаззификацию, чтобы получить окончательное значение уровня нагрева.
    
    Аргументы:
    - heating_values: степени принадлежности уровня нагрева к каждому терму
    - heating_membership_functions: функции принадлежности для "уровня нагрева"
    
    Возвращает:
    - дефаззифицированное значение уровня нагрева (вещественное число)
    """
    numerator = 0
    denominator = 0
    
    for term, membership_value in heating_values.items():
        if membership_value > 0:
            points = heating_membership_functions[term]
            # Центр тяжести треугольной или трапециевидной функции принадлежности
            x_values = [x for x, y in points]
            center = sum(x_values) / len(x_values)  # Берем центр графика функции принадлежности
            numerator += center * membership_value
            denominator += membership_value
    
    if denominator == 0:
        return 0  # защита от деления на 0
    
    return numerator / denominator

def task(temperature_json, heating_json, rules_json, current_temperature):
    """
    Основная функция нечеткого управления.
    
    Аргументы:
    - temperature_json: JSON-строка с функциями принадлежности для переменной "температура"
    - heating_json: JSON-строка с функциями принадлежности для переменной "уровень нагрева"
    - rules_json: JSON-строка с логическими правилами управления
    - current_temperature: текущее значение температуры (вещественное число)
    
    Возвращает:
    - значение уровня нагрева (вещественное число)
    """
    # Парсинг входных JSON-строк
    temperature_functions = json.loads(temperature_json)
    heating_functions = json.loads(heating_json)
    rules = json.loads(rules_json)
    
    # 1. Фаззификация
    fuzzy_temperature = fuzzification(current_temperature, temperature_functions)
    
    # 2. Применение правил
    heating_values = apply_rule(fuzzy_temperature, rules, heating_functions)
    
    # 3. Дефаззификация
    heating_level = defuzzification(heating_values, heating_functions)
    
    return heating_level

# Пример данных для тестирования
temperature_json = """{
    "холодно": [[0, 1], [16, 1], [20, 0], [50, 0]],
    "комфортно": [[16, 0], [20, 1], [22, 1], [26, 0]],
    "жарко": [[0, 0], [22, 0], [26, 1], [50, 1]]
}"""

heating_json = """{
    "слабо": [[0, 1], [6, 1], [10, 0], [20, 0]],
    "умеренно": [[6, 0], [10, 1], [12, 1], [16, 0]],
    "интенсивно": [[0, 0], [12, 0], [16, 1], [20, 1]]
}"""

rules_json = """{
    "холодно": "интенсивно",
    "комфортно": "умеренно",
    "жарко": "слабо"
}"""

current_temperature = 17

# Вызов функции управления
heating_level = task(temperature_json, heating_json, rules_json, current_temperature)
print(f"Уровень нагрева: {heating_level}")
