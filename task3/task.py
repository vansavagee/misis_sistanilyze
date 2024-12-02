import csv
import sys
import math

def parse_matrix(file_path):
    matrix = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            matrix.append(list(map(float, row)))
    return matrix

def calculate_entropy(matrix):
    n = len(matrix)
    k = len(matrix[0])
    entropy = 0.0
    for i in range(n):
        for j in range(k):
            l_ij = matrix[i][j]
            if l_ij != 0:
                entropy -= (l_ij / (n - 1)) * math.log2(l_ij / (n - 1))
    return round(entropy, 1)

def task(file_path):
    matrix = parse_matrix(file_path)
    entropy = calculate_entropy(matrix)
    return entropy

def main():
    if len(sys.argv) != 2:
        print("Usage: python task.py <path_to_csv_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    entropy = task(file_path)
    print(entropy)

if __name__ == "__main__":
    main()
