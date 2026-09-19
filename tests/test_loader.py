from data_engine.loader import load_file

df = load_file("data/sample.csv")

# df = load_file('data/retail_sales_dataset.xlsx')

print(df)

print("\nShape:", df.shape)

print("\nColumns:", df.columns.tolist())