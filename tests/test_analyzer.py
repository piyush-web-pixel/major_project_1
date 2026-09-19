from data_engine.loader import load_file
from data_engine.profiler import profile_data
from data_engine.column_detector import detect_columns
from data_engine.cleaner import clean_data
from data_engine.analyzer import analyze_data


# =========================================================
# LOAD
# =========================================================

df = load_file("data/sample.csv")

# df = load_file('data/retail_sales_dataset.xlsx')

# =========================================================
# DETECT
# =========================================================

detected_columns = detect_columns(df)


# =========================================================
# CLEAN
# =========================================================

cleaned_df, cleaning_report = clean_data(
    df,
    detected_columns
)


# =========================================================
# ANALYZE
# =========================================================

analysis = analyze_data(
    cleaned_df,
    detected_columns
)


# =========================================================
# NUMERIC
# =========================================================

print("\n========== NUMERIC ANALYSIS ==========\n")

for column, information in analysis[
    "numeric"
].items():

    print(f"\n{column}")

    for key, value in information.items():

        print(
            f"  {key}: {value}"
        )


# =========================================================
# CATEGORICAL
# =========================================================

print("\n========== CATEGORICAL ANALYSIS ==========\n")

for column, information in analysis[
    "categorical"
].items():

    print(f"\n{column}")

    print(
        "  Unique:",
        information["unique_values"]
    )

    print(
        "  Top Value:",
        information["top_value"]
    )

    print(
        "  Top Count:",
        information["top_value_count"]
    )

    print(
        "  Distribution:",
        information["distribution"]
    )


# =========================================================
# BINARY
# =========================================================

print("\n========== BINARY ANALYSIS ==========\n")

for column, information in analysis[
    "binary"
].items():

    print(f"\n{column}")

    print(
        "  Distribution:",
        information["distribution"]
    )


# =========================================================
# DATE
# =========================================================

print("\n========== DATE ANALYSIS ==========\n")

for column, information in analysis[
    "date"
].items():

    print(f"\n{column}")

    for key, value in information.items():

        print(
            f"  {key}: {value}"
        )


# =========================================================
# CORRELATION
# =========================================================
print("\n========== CORRELATION ANALYSIS ==========\n")

for relationship in analysis["correlations"]:

    print(
        f"{relationship['column_1']} ↔ "
        f"{relationship['column_2']} → "
        f"{relationship['correlation']}"
    )