import sys
import os
from exchange import ExchangeEngine

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file_path>")
        sys.exit(1)

    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found.")
        sys.exit(1)

    engine = ExchangeEngine()

    try:
        with open(input_file, 'r') as f:
            for line in f:
                engine.process_line(line)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()