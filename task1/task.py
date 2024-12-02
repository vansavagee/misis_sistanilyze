import csv
import sys

def main():
    if len(sys.argv) != 4:
        print("Usage: python script.py <csv_file_path> <row_number> <column_number>")
        sys.exit(1)

    file_path = sys.argv[1]
    row_number = int(sys.argv[2])
    column_number = int(sys.argv[3])

    try:
        with open(file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)

            # Check if the specified row and column exist
            if row_number < 1 or row_number > len(data):
                print(f"Error: Row {row_number} is out of range.")
                sys.exit(1)
            if column_number < 1 or column_number > len(data[0]):
                print(f"Error: Column {column_number} is out of range.")
                sys.exit(1)

            # Access the specific cell
            value = data[row_number - 1][column_number - 1]
            print(value)

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
