import pandas as pd


COLUMN_ALIASES = {
    "expense_date": [
        "expense_date",
        "date",
        "transaction_date",
        "transaction date",
        "expense date"
    ],

    "category": [
        "category",
        "type",
        "expense_category",
        "expense category"
    ],

    "description": [
        "description",
        "details",
        "detail",
        "expense",
        "item",
        "notes"
    ],

    "amount": [
        "amount",
        "debit",
        "expense_amount",
        "expense amount",
        "value"
    ],

    "payment_method": [
        "payment_method",
        "payment method",
        "payment",
        "mode",
        "transaction_mode"
    ],

    "merchant": [
        "merchant",
        "merchant_name",
        "merchant name",
        "store",
        "vendor"
    ]
}


REQUIRED_COLUMNS = [
    "expense_date",
    "category",
    "amount"
]


def normalize_column_name(column):

    return (
        str(column)
        .strip()
        .lower()
        .replace("_", " ")
    )


def map_columns(df):

    df = df.copy()

    normalized_columns = {
        column: normalize_column_name(column)
        for column in df.columns
    }

    rename_map = {}

    for standard_name, aliases in COLUMN_ALIASES.items():

        normalized_aliases = [
            normalize_column_name(alias)
            for alias in aliases
        ]

        for original_column, normalized_column in normalized_columns.items():

            if normalized_column in normalized_aliases:

                rename_map[original_column] = standard_name
                break

    df = df.rename(
        columns=rename_map
    )

    return df


def validate_expense_data(df):

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    return (
        len(missing_columns) == 0,
        missing_columns
    )


def clean_expense_data(df):

    df = df.copy()

    # Convert date
    df["expense_date"] = pd.to_datetime(
        df["expense_date"],
        errors="coerce"
    )

    # Convert amount
    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    # Remove rows without valid date or amount
    df = df.dropna(
        subset=[
            "expense_date",
            "amount"
        ]
    )

    # Category
    df["category"] = (
        df["category"]
        .fillna("Uncategorized")
        .astype(str)
        .str.strip()
    )

    # Description
    if "description" not in df.columns:
        df["description"] = "No description"
    else:
        df["description"] = (
            df["description"]
            .fillna("No description")
            .astype(str)
            .str.strip()
        )

    # Payment method
    if "payment_method" not in df.columns:
        df["payment_method"] = "Unknown"
    else:
        df["payment_method"] = (
            df["payment_method"]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )

    # Merchant
    if "merchant" not in df.columns:
        df["merchant"] = "Unknown"
    else:
        df["merchant"] = (
            df["merchant"]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )

    return df