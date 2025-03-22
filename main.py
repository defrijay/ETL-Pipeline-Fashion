# Import fungsi-fungsi yang diperlukan dari modul utils
from utils.extract import extract_data
from utils.transform import transform_data
from utils.load import load_to_csv, load_to_google_sheets

def main():
    try:
        data = extract_data()
        transformed_data = transform_data(data)
        load_to_csv(transformed_data)
    except Exception as e:
        print(f"An error occurred during the ETL process: {e}")

if __name__ == '__main__':
    main()