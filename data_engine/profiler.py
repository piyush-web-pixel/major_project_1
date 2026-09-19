import pandas as pd


def profile_data(df):

    profile = {}

    # -----------------------------
    # BASIC INFORMATION
    # -----------------------------

    profile["rows"] = df.shape[0]
    profile["columns"] = df.shape[1]

    profile["column_names"] = df.columns.tolist()

    # -----------------------------
    # DATA TYPES
    # -----------------------------

    profile["data_types"] = {
        column: str(dtype)
        for column, dtype in df.dtypes.items()
    }

    # -----------------------------
    # MISSING VALUES
    # -----------------------------

    missing = df.isna().sum()

    profile["missing_values"] = {
        column: int(value)
        for column, value in missing.items()
        if value > 0
    }

    # -----------------------------
    # DUPLICATES
    # -----------------------------

    profile["duplicate_rows"] = int(
        df.duplicated().sum()
    )

    # -----------------------------
    # NUMERIC COLUMNS
    # -----------------------------

    profile["numeric_columns"] = (
        df.select_dtypes(
            include="number"
        ).columns.tolist()
    )

    # -----------------------------
    # CATEGORICAL COLUMNS
    # -----------------------------

    profile["categorical_columns"] = (
        df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()
    )

    # -----------------------------
    # UNIQUE VALUES
    # -----------------------------

    profile["unique_values"] = {
        column: int(df[column].nunique())
        for column in df.columns
    }

    return profile