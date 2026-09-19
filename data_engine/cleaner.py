import pandas as pd
import numpy as np


# =========================================================
# MISSING VALUE HANDLING
# =========================================================

def handle_missing_values(df, detected_columns):

    df = df.copy()

    report = {
        "columns_dropped": [],
        "values_filled": {},
        "total_values_filled": 0
    }

    for column in df.columns:

        missing_count = df[column].isna().sum()

        if missing_count == 0:
            continue

        missing_percentage = (
            missing_count / len(df)
        ) * 100

        column_type = detected_columns[column]["type"]

        # -------------------------------------------------
        # More than 30% missing → drop column
        # -------------------------------------------------

        if missing_percentage > 30:

            df.drop(
                columns=[column],
                inplace=True
            )

            report["columns_dropped"].append(
                {
                    "column": column,
                    "missing_percentage": round(
                        missing_percentage,
                        2
                    )
                }
            )

        # -------------------------------------------------
        # Numeric → median
        # -------------------------------------------------

        elif column_type in ["numeric", "binary"]:

            fill_value = df[column].median()

            df[column] = df[column].fillna(
                fill_value
            )

            report["values_filled"][column] = {
                "method": "median",
                "count": int(missing_count)
            }

            report["total_values_filled"] += int(
                missing_count
            )

        # -------------------------------------------------
        # Categorical / identifier / text → mode
        # -------------------------------------------------

        elif column_type in [
            "categorical",
            "identifier",
            "text"
        ]:

            mode_values = df[column].mode()

            if len(mode_values) > 0:

                fill_value = mode_values.iloc[0]

                df[column] = df[column].fillna(
                    fill_value
                )

                report["values_filled"][column] = {
                    "method": "mode",
                    "count": int(missing_count)
                }

                report["total_values_filled"] += int(
                    missing_count
                )

        # -------------------------------------------------
        # Date → forward fill
        # -------------------------------------------------

        elif column_type == "date":

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            df[column] = df[column].ffill()

            report["values_filled"][column] = {
                "method": "forward_fill",
                "count": int(missing_count)
            }

            report["total_values_filled"] += int(
                missing_count
            )

    return df, report


# =========================================================
# DUPLICATE HANDLING
# =========================================================

def remove_duplicates(df):

    df = df.copy()

    duplicate_count = int(
        df.duplicated().sum()
    )

    df = df.drop_duplicates()

    report = {
        "duplicates_removed": duplicate_count
    }

    return df, report


# =========================================================
# DATE CONVERSION
# =========================================================

def convert_date_columns(df, detected_columns):

    df = df.copy()

    converted_columns = []

    for column, information in detected_columns.items():

        if (
            column in df.columns
            and information["type"] == "date"
        ):

            before_dtype = df[column].dtype

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            if not pd.api.types.is_datetime64_any_dtype(
                df[column]
            ):
                continue

            converted_columns.append(column)

    report = {
        "date_columns_converted": converted_columns
    }

    return df, report


# =========================================================
# IQR OUTLIER DETECTION
# =========================================================

def detect_outliers(df, detected_columns):

    outlier_report = {}

    total_outliers = 0

    for column, information in detected_columns.items():

        if column not in df.columns:
            continue

        # Only numeric columns
        if information["type"] != "numeric":
            continue

        series = df[column].dropna()

        if len(series) == 0:
            continue

        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)

        IQR = Q3 - Q1

        # If all values are same
        if IQR == 0:
            continue

        lower_bound = Q1 - (1.5 * IQR)
        upper_bound = Q3 + (1.5 * IQR)

        outlier_mask = (
            (df[column] < lower_bound)
            |
            (df[column] > upper_bound)
        )

        outlier_count = int(
            outlier_mask.sum()
        )

        if outlier_count > 0:

            outlier_percentage = (
                outlier_count / len(df)
            ) * 100

            outlier_report[column] = {

                "outliers": outlier_count,

                "percentage": round(
                    outlier_percentage,
                    2
                ),

                "lower_bound": float(
                    lower_bound
                ),

                "upper_bound": float(
                    upper_bound
                )
            }

            total_outliers += outlier_count

    return outlier_report, total_outliers


# =========================================================
# MAIN CLEANING FUNCTION
# =========================================================

def clean_data(df, detected_columns):

    original_rows = len(df)
    original_columns = len(df.columns)

    # -----------------------------------------------------
    # 1. Missing values
    # -----------------------------------------------------

    df, missing_report = handle_missing_values(
        df,
        detected_columns
    )

    # -----------------------------------------------------
    # 2. Duplicates
    # -----------------------------------------------------

    df, duplicate_report = remove_duplicates(
        df
    )

    # -----------------------------------------------------
    # 3. Date conversion
    # -----------------------------------------------------

    df, date_report = convert_date_columns(
        df,
        detected_columns
    )

    # -----------------------------------------------------
    # 4. Outlier detection
    # -----------------------------------------------------

    outlier_report, total_outliers = detect_outliers(
        df,
        detected_columns
    )

    # -----------------------------------------------------
    # FINAL REPORT
    # -----------------------------------------------------

    cleaning_report = {

        "original_rows": original_rows,

        "final_rows": len(df),

        "original_columns": original_columns,

        "final_columns": len(df.columns),

        "rows_removed": (
            original_rows - len(df)
        ),

        "columns_removed": (
            original_columns - len(df.columns)
        ),

        "missing_values": missing_report,

        "duplicates": duplicate_report,

        "dates": date_report,

        "outliers": {
            "total": total_outliers,
            "columns": outlier_report
        }
    }

    return df, cleaning_report