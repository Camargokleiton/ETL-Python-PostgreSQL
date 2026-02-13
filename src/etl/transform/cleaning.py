import re
from typing import Optional, List
import pandas as pd


def normalize_phone(phone: Optional[str]) -> Optional[str]:
    """
    Normalize phone number to Brazilian standard:
    55 + DDD + number (13 digits).

    Examples:
        "(41) 99999-8888" -> "5541999998888"
        "41999998888"     -> "5541999998888"

    Returns None if invalid.
    """
    if pd.isna(phone):
        return None
    
    phone = re.sub(r"\D", "", phone)

    if len(phone) == 11:  
        phone = "55" + phone
    
    if len(phone) == 13:
        return phone
    
    return None



def fill_missing_emails(
    df: pd.DataFrame,
    col_name: str = "email",
    name_col: str = "name",
    domain: str = "@email.com"
) -> pd.DataFrame:
    """
    Fill missing emails by generating them from the name.
    Example: "Ana Silva" -> "anasilva@email.com"
    """
    mask = df[col_name].isnull()
    
    df.loc[mask, col_name] = (
        df.loc[mask, name_col]
        .str.lower()
        .str.replace(r"\s+", "", regex=True)
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")

        + domain
    )
    
    return df


def fill_missing_phones(
    df: pd.DataFrame,
    col_name: str = "phone",
    default_number: str = "5541900000000"
) -> pd.DataFrame:
    """
    Fill missing or empty phone numbers with a default value.
    """
    mask = (df[col_name].isnull()) | (df[col_name].astype(str).str.strip() == "")
    df.loc[mask, col_name] = default_number
    return df


def fill_invalid_birth_dates(
    df: pd.DataFrame,
    col_name: str = "birth_date",
    default_date: str = "1990-01-01"
) -> pd.DataFrame:
    """
    Replace invalid or future birth dates with a default date.
    """
    df[col_name] = pd.to_datetime(df[col_name], errors='coerce')
    mask = (df[col_name].isnull()) | (df[col_name] > pd.Timestamp.now())
    df.loc[mask, col_name] = pd.to_datetime(default_date)
    return df


def standardize_payment_methods(
    df: pd.DataFrame,
    col_name: str = "payment_method"
) -> pd.DataFrame:
    """
    Standardize payment methods to snake_case.
    Invalid values become 'other'.
    """
    valid_methods = {"credit_card", "debit_card", "paypal", "bank_transfer", "cash"}
    df[col_name] = (
    df[col_name]
    .fillna("other")
    .astype(str)
    .str.lower()
    .str.replace(" ", "_")
)
    mask = ~df[col_name].isin(valid_methods)
    df.loc[mask, col_name] = "other"
    return df   


def fill_missing_status(
    df: pd.DataFrame,
    col_name: str = "status",
    default_status: str = "pending"
) -> pd.DataFrame:
    """
    Fill missing or empty status with 'pending'.
    """
    mask = df[col_name].isnull() | (df[col_name].astype(str).str.strip() == "")
    df.loc[mask, col_name] = default_status
    return df


def convert_amount_to_float(
    df: pd.DataFrame,
    col_name: str = "amount"
) -> pd.DataFrame:
    """
    Convert amount column to float.
    Invalid values become NaN.
    """
    df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
    return df


def fill_negative_amounts(
    df: pd.DataFrame,
    col_name: str = "amount",
    default_value: float = 0.0
) -> pd.DataFrame:
    """
    Replace negative values with 0.0.
    """
    mask = df[col_name] < 0
    df.loc[mask, col_name] = default_value
    return df


def remove_duplicates(
    df: pd.DataFrame,
    subset_cols: List[str] = ["id"]
) -> pd.DataFrame:
    """
    Remove duplicate records based on given columns.
    """
    df = df.drop_duplicates(subset=subset_cols)
    return df


def fill_missing_order_dates(
    df: pd.DataFrame,
    col_name: str = "order_date",
    default_date: str = "2020-01-01"
) -> pd.DataFrame:
    """
    Fill missing order dates with a default date.
    """
    df[col_name] = pd.to_datetime(df[col_name], errors='coerce')
    mask = df[col_name].isnull()
    df.loc[mask, col_name] = pd.to_datetime(default_date)
    return df


def standardize_birth_dates(
    df: pd.DataFrame,
    col_name: str = "birth_date"
) -> pd.DataFrame:
    """
    Convert multiple date formats to ISO format YYYY-MM-DD.
    Accepts Brazilian formats (DD/MM/YYYY).
    Invalid dates become NaT.
    """
    df[col_name] = pd.to_datetime(
        df[col_name],
        errors="coerce",
        dayfirst=True
    )
    df[col_name] = df[col_name].dt.strftime("%Y-%m-%d")
    return df


