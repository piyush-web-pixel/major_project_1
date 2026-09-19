import pandas as pd
from pathlib import Path


SUPPORTED_EXTENSIONS = [".csv", ".xlsx", ".xls"]


def load_file(file_path):
    """
    Load CSV or Excel file into a Pandas DataFrame.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    extension = file_path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            "Unsupported file format. "
            "Only CSV and Excel files are supported."
        )

    if extension == ".csv":
        df = pd.read_csv(file_path)

    elif extension in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path)

    return df