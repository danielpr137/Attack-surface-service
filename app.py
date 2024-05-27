import sys
from app import app
# from app import app
from app.cloud_env import load_cloud_env

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        load_cloud_env(f'inputs/{input_file}')
    else:
        print("Please provide the input file as an argument.")
        print("Example: python app.py input-2.json")
        sys.exit(1)

    app.run()