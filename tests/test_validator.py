import pandas as pd

from data_engine.validator import (
    validate_file_path,
    validate_dataframe,
    validate_dataset
)


# ==========================================
# TEST FILE VALIDATION
# ==========================================

validate_file_path(
    "data/sample.csv"
)

print(
    "File validation: PASSED"
)


# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(
    "data/sample.csv"
)


# ==========================================
# TEST DATAFRAME
# ==========================================

validate_dataframe(df)

print(
    "DataFrame validation: PASSED"
)


# ==========================================
# COMPLETE VALIDATION
# ==========================================

report = validate_dataset(df)

print(
    "\n========== VALIDATION REPORT =========="
)

print(
    "Valid:",
    report["valid"]
)

print(
    "Rows:",
    report["rows"]
)

print(
    "Columns:",
    report["columns"]
)

print(
    "Duplicate Columns:",
    report["duplicate_columns"]
)

print(
    "Empty Columns:",
    report["empty_columns"]
)

print(
    "Warnings:",
    report["warnings"]
)