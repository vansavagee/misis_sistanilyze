import json

def flatten_ranking(ranking):
    """Разворачивает вложенные списки в одномерный список."""
    flat_list = []
    for item in ranking:
        if isinstance(item, list):
            flat_list.extend(flatten_ranking(item))
        else:
            flat_list.append(item)
    return flat_list

def find_conflict(ranking1, ranking2):
    """Находит конфликты между двумя ранжировками."""
    flat_ranking1 = flatten_ranking(ranking1)
    flat_ranking2 = flatten_ranking(ranking2)

    conflicts = []
    for i, elem1 in enumerate(flat_ranking1):
        for j, elem2 in enumerate(flat_ranking1[i + 1:], start=i + 1):
            # Проверяем порядок в первой ранжировке против второй
            if flat_ranking2.index(elem1) > flat_ranking2.index(elem2):
                conflicts.append([str(elem1), str(elem2)])
    return conflicts

def main(json1, json2):
    try:
        ranking1 = json.loads(json1)
        ranking2 = json.loads(json2)
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON input"})

    conflicts = find_conflict(ranking1, ranking2)
    return json.dumps(conflicts)

if __name__ == "__main__":
    json1 = '[1, [2, 3], 4, [5, 6, 7], 8, 9, 10]'
    json2 = '[[1, 2], [3, 4, 5], 6, 7, 9, [8, 10]]'

    print(main(json1, json2))
