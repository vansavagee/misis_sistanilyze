import csv
import sys
from collections import defaultdict, deque

def parse_graph(file_path):
    edges = []
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            edges.append(tuple(map(int, row)))
    return edges

def calculate_relationships(edges, node_count):
    adjacency_list = defaultdict(list)
    reverse_adjacency_list = defaultdict(list)
    for parent, child in edges:
        adjacency_list[parent].append(child)
        reverse_adjacency_list[child].append(parent)

    l_values = [[0] * 5 for _ in range(node_count)]

    for parent, children in adjacency_list.items():
        for child in children:
            l_values[parent - 1][0] += 1
            l_values[child - 1][1] += 1

    for node in range(1, node_count + 1):
        visited = set()
        queue = deque([(node, 0)])
        while queue:
            current, depth = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            if depth > 1:
                l_values[node - 1][2] += 1
                l_values[current - 1][3] += 1
            for neighbor in adjacency_list[current]:
                if neighbor not in visited:
                    queue.append((neighbor, depth + 1))

    for node in range(1, node_count + 1):
        parents = reverse_adjacency_list[node]
        siblings = set()
        for parent in parents:
            siblings.update(adjacency_list[parent])
        siblings.discard(node)
        l_values[node - 1][4] = len(siblings)

    return l_values

def format_output(l_values):
    output = []
    for row in l_values:
        output.append(','.join(map(str, row)))
    return '\n'.join(output)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_csv_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    edges = parse_graph(file_path)
    node_count = max(max(pair) for pair in edges)
    l_values = calculate_relationships(edges, node_count)
    print(format_output(l_values))

if __name__ == "__main__":
    main()
