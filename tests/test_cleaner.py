from data_engine.loader import load_file
from data_engine.profiler import profile_data
from data_engine.column_detector import detect_columns
from data_engine.cleaner import clean_data


# =========================================================
# LOAD DATA
# =========================================================

df = load_file("data/sample.csv")


# =========================================================
# PROFILE
# =========================================================

profile = profile_data(df)


# =========================================================
# DETECT COLUMN TYPES
# =========================================================

detected_columns = detect_columns(df)


# =========================================================
# CLEAN DATA
# =========================================================

cleaned_df, report = clean_data(
    df,
    detected_columns
)


# =========================================================
# PRINT RESULTS
# =========================================================

print("\n========== CLEANING SUMMARY ==========\n")

print(
    "Original Rows:",
    report["original_rows"]
)

print(
    "Final Rows:",
    report["final_rows"]
)

print(
    "Rows Removed:",
    report["rows_removed"]
)

print(
    "Original Columns:",
    report["original_columns"]
)

print(
    "Final Columns:",
    report["final_columns"]
)

print(
    "Columns Removed:",
    report["columns_removed"]
)


# =========================================================
# MISSING VALUES
# =========================================================

print("\nMissing Value Handling:")

print(
    report["missing_values"]
)


# =========================================================
# DUPLICATES
# =========================================================

print("\nDuplicate Handling:")

print(
    report["duplicates"]
)


# =========================================================
# DATE CONVERSION
# =========================================================

print("\nDate Conversion:")

print(
    report["dates"]
)


# =========================================================
# OUTLIERS
# =========================================================

print("\nOutlier Detection:")

print(
    "Total Outliers:",
    report["outliers"]["total"]
)
for column, information in report[
    "outliers"
]["columns"].items():

    print(
        f"{column} → "
        f"Outliers: {information['outliers']} "
        f"({information['percentage']}%) | "
        f"Lower: {information['lower_bound']:.2f} | "
        f"Upper: {information['upper_bound']:.2f}"
    )

# =========================================================
# FINAL DATA TYPES
# =========================================================

print("\nFinal Data Types:")

print(
    cleaned_df.dtypes
)