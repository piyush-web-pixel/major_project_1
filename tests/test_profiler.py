from data_engine.loader import load_file
from data_engine.profiler import profile_data

df = load_file("data/sample.csv")

# df = load_file('data/retail_sales_dataset.xlsx')
profile = profile_data(df)


print("\n========== DATASET PROFILE ==========\n")

print("Rows:", profile["rows"])

print("Columns:", profile["columns"])

print("\nColumn Names:")
print(profile["column_names"])

print("\nData Types:")
for column, dtype in profile["data_types"].items():
    print(f"{column} → {dtype}")

print("\nMissing Values:")
print(profile["missing_values"])

print("\nDuplicate Rows:")
print(profile["duplicate_rows"])

print("\nNumeric Columns:")
print(profile["numeric_columns"])

print("\nCategorical Columns:")
print(profile["categorical_columns"])

print("\nUnique Values:")
for column, count in profile["unique_values"].items():
    print(f"{column} → {count}")