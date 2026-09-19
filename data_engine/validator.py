import pandas as pd


SUPPORTED_EXTENSIONS = [
    ".csv",
    ".xlsx",
    ".xls"
]


def validate_file_path(file_path):
    """
    Validate file path and extension.
    """

    from pathlib import Path

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    if not path.is_file():
        raise ValueError(
            f"Provided path is not a file: {file_path}"
        )

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            "Unsupported file format. "
            "Only CSV and Excel files are supported."
        )

    return True


def validate_dataframe(df):
    """
    Validate basic dataframe structure.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            "Input must be a Pandas DataFrame."
        )

    if df.empty:
        raise ValueError(
            "Dataset is empty."
        )

    if len(df.columns) == 0:
        raise ValueError(
            "Dataset contains no columns."
        )

    return True


def find_duplicate_columns(df):
    """
    Find duplicate column names.
    """

    duplicate_columns = (
        df.columns[
            df.columns.duplicated()
        ]
        .tolist()
    )

    return duplicate_columns


def find_empty_columns(df):
    """
    Find columns containing no usable values.
    """

    empty_columns = []

    for column in df.columns:

        if df[column].isna().all():

            empty_columns.append(
                column
            )

    return empty_columns


def validate_dataset(
    df,
    minimum_rows=2
):
    """
    Perform complete dataset validation.
    """

    validate_dataframe(df)

    if len(df) < minimum_rows:

        raise ValueError(
            f"Dataset must contain at least "
            f"{minimum_rows} rows."
        )

    duplicate_columns = (
        find_duplicate_columns(df)
    )

    if duplicate_columns:

        raise ValueError(
            "Duplicate column names detected: "
            f"{duplicate_columns}"
        )

    empty_columns = (
        find_empty_columns(df)
    )

    report = {

        "valid": True,

        "rows": len(df),

        "columns": len(df.columns),

        "duplicate_columns": (
            duplicate_columns
        ),

        "empty_columns": (
            empty_columns
        ),

        "warnings": []

    }

    if empty_columns:

        report["warnings"].append(
            f"{len(empty_columns)} completely "
            "empty column(s) detected."
        )

    return report