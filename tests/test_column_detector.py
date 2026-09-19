from data_engine.loader import load_file
from data_engine.column_detector import detect_columns

df = load_file("data/sample.csv")

# df = load_file('data/retail_sales_dataset.xlsx')

result = detect_columns(df)


print("\n========== COLUMN DETECTION ==========\n")


for column, information in result.items():

    print(
        f"{column} → "
        f"{information['type']} | "
        f"Confidence: {information['confidence']}% | "
        f"Unique: {information['unique_values']} | "
        f"Missing: {information['missing_values']}"
    )