import pandas as pd
import re


# =========================================================
# NORMALIZE COLUMN NAME
# =========================================================

def normalize_column_name(column):

    column = str(column).strip().lower()

    column = re.sub(
        r"[^a-z0-9]+",
        "_",
        column
    )

    return column.strip("_")


# =========================================================
# DATE DETECTION
# =========================================================

def is_date_column(column_name, series):

    name = normalize_column_name(column_name)

    date_keywords = [
        "date",
        "time",
        "timestamp",
        "created",
        "updated",
        "modified",
        "birth",
        "dob",
        "join",
        "joining",
        "purchase",
        "transaction",
        "order"
    ]

    words = name.split("_")

    keyword_match = any(
        keyword in words
        for keyword in date_keywords
    )

    # Already datetime
    if pd.api.types.is_datetime64_any_dtype(series):

        return True, 100

    # Try parsing string/object data
    if (
        pd.api.types.is_object_dtype(series)
        or pd.api.types.is_string_dtype(series)
    ):

        sample = (
            series
            .dropna()
            .astype(str)
            .head(100)
        )

        if len(sample) == 0:
            return False, 0

        parsed = pd.to_datetime(
            sample,
            format="mixed",
            errors="coerce"
        )

        valid_ratio = parsed.notna().mean()

        if valid_ratio >= 0.80:

            confidence = int(
                valid_ratio * 100
            )

            if keyword_match:

                confidence = min(
                    100,
                    confidence + 5
                )

            return True, confidence

    # Strong semantic date signal
    if keyword_match:

        return True, 85

    return False, 0


# =========================================================
# IDENTIFIER DETECTION
# =========================================================
def is_identifier_column(
    column_name,
    series
):

    name = normalize_column_name(
        column_name
    )

    words = name.split("_")

    # Strong identifier signals
    identifier_keywords = [
        "id",
        "identifier",
        "uuid",
        "guid",
        "sku",
        "key"
    ]

    # Exact word match
    if any(
        keyword in words
        for keyword in identifier_keywords
    ):
        return True, 98

    # Handle names like:
    # CustomerID
    # ProductID
    # EmployeeID
    # UserID
    # OrderID

    compact_identifier_patterns = [
        r".*id$",
        r".*uuid$",
        r".*guid$",
        r".*sku$"
    ]

    for pattern in compact_identifier_patterns:

        if re.fullmatch(
            pattern,
            name
        ):

            return True, 98

    # Code / number / no
    code_keywords = [
        "code",
        "number",
        "no"
    ]

    if any(
        keyword in words
        for keyword in code_keywords
    ):

        unique_ratio = (
            series.nunique(dropna=True)
            / max(len(series), 1)
        )

        if unique_ratio >= 0.50:

            return True, 90

    return False, 0

# =========================================================
# BINARY DETECTION
# =========================================================

def is_binary_column(series):

    unique_values = (
        series
        .dropna()
        .unique()
    )

    if len(unique_values) != 2:

        return False, 0

    return True, 95


# =========================================================
# CATEGORICAL DETECTION
# =========================================================

def is_categorical_column(
    column_name,
    series
):

    name = normalize_column_name(
        column_name
    )

    words = name.split("_")

    # Strong categorical semantic signals
    categorical_keywords = [

        "category",
        "type",
        "class",
        "group",
        "segment",

        "gender",
        "sex",

        "city",
        "town",
        "location",
        "place",

        "country",
        "state",
        "region",
        "district",

        "department",
        "role",
        "position",

        "status",
        "level",
        "grade",

        "color",
        "colour",

        "brand",

        "product",
        "customer",

        "weather",
        "season"
    ]

    if any(
        keyword in words
        for keyword in categorical_keywords
    ):

        return True, 95

    # Object/string columns
    if (
        pd.api.types.is_object_dtype(series)
        or pd.api.types.is_string_dtype(series)
        or str(series.dtype) == "category"
    ):

        unique_count = (
            series.nunique(dropna=True)
        )

        row_count = len(series)

        if row_count == 0:

            return False, 0

        unique_ratio = (
            unique_count / row_count
        )

        # Low / medium cardinality
        if unique_count <= 50:

            return True, 90

        # Moderate cardinality
        if unique_ratio <= 0.20:

            return True, 80

    return False, 0


# =========================================================
# NUMERIC DETECTION
# =========================================================

def is_numeric_column(series):

    if pd.api.types.is_numeric_dtype(series):

        return True, 95

    return False, 0


# =========================================================
# TEXT DETECTION
# =========================================================

def is_text_column(series):

    if (
        pd.api.types.is_object_dtype(series)
        or pd.api.types.is_string_dtype(series)
    ):

        return True, 60

    return False, 0


# =========================================================
# MAIN COLUMN TYPE DETECTOR
# =========================================================

def detect_column_type(
    column_name,
    series
):

    # -----------------------------------------------------
    # DATE
    # -----------------------------------------------------

    result, confidence = is_date_column(
        column_name,
        series
    )

    if result:

        return "date", confidence


    # -----------------------------------------------------
    # IDENTIFIER
    # -----------------------------------------------------

    result, confidence = is_identifier_column(
        column_name,
        series
    )

    if result:

        return "identifier", confidence


    # -----------------------------------------------------
    # BINARY
    # -----------------------------------------------------

    result, confidence = is_binary_column(
        series
    )

    if result:

        return "binary", confidence


    # -----------------------------------------------------
    # NUMERIC
    # -----------------------------------------------------

    result, confidence = is_numeric_column(
        series
    )

    if result:

        return "numeric", confidence


    # -----------------------------------------------------
    # CATEGORICAL
    # -----------------------------------------------------

    result, confidence = is_categorical_column(
        column_name,
        series
    )

    if result:

        return "categorical", confidence


    # -----------------------------------------------------
    # TEXT
    # -----------------------------------------------------

    result, confidence = is_text_column(
        series
    )

    if result:

        return "text", confidence


    # -----------------------------------------------------
    # UNKNOWN
    # -----------------------------------------------------

    return "unknown", 50


# =========================================================
# DETECT ALL COLUMNS
# =========================================================

def detect_columns(df):

    detected_columns = {}

    for column in df.columns:

        column_type, confidence = (
            detect_column_type(
                column,
                df[column]
            )
        )

        detected_columns[column] = {

            "type": column_type,

            "confidence": confidence,

            "unique_values": int(
                df[column].nunique(
                    dropna=True
                )
            ),

            "missing_values": int(
                df[column].isna().sum()
            )
        }

    return detected_columns