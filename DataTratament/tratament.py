
import re
import pandas as pd


def normalize_phone(phone):
    if pd.isna(phone):
        return None
    
    phone = re.sub(r"\D", "", phone)

    if len(phone) == 11:  
        phone = "55" + phone
    
    if len(phone) == 13:
        return phone
    
    return None


def fill_missing_emails(df, col_name="email", name_col="name", domain="@email.com"):
    mask = df[col_name].isnull()
    
    df.loc[mask, col_name] = (
        df.loc[mask, name_col]
        .str.lower()
        .str.replace(" ", "")
        + domain
    )
    
    return df

def fill_missing_phones(df, col_name="phone", default_number="5541900000000"):
    mask = (df[col_name].isnull()) | (df[col_name].astype(str).str.strip() == "")
    df.loc[mask, col_name] = default_number
    return df

def fill_invalid_birth_dates(df, col_name="birth_date", default_date="1990-01-01"):
    df[col_name] = pd.to_datetime(df[col_name], errors='coerce')
    mask = (df[col_name].isnull()) | (df[col_name] > pd.Timestamp.now())
    df.loc[mask, col_name] = pd.to_datetime(default_date)
    return df

def standardize_payment_methods(df, col_name="payment_method"):
    valid_methods = {"credit_card", "debit_card", "paypal", "bank_transfer", "cash"}
    df[col_name] = df[col_name].str.lower().str.replace(" ", "_")
    mask = ~df[col_name].isin(valid_methods)
    df.loc[mask, col_name] = "other"
    return df   

def fill_missing_status(df, col_name="status", default_status="pending"):
    mask = df[col_name].isnull() | (df[col_name].astype(str).str.strip() == "")
    df.loc[mask, col_name] = default_status
    return df

def convert_amount_to_float(df, col_name="amount"):
    df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
    return df

def fill_negative_amounts(df, col_name="amount", default_value=0.0):
    mask = df[col_name] < 0
    df.loc[mask, col_name] = default_value
    return df

def remove_duplicate(df, subset_cols=["id"]):
    df = df.drop_duplicates(subset=subset_cols)
    return df

def fill_missing_order_dates(df, col_name="order_date", default_date="2020-01-01"):
    df[col_name] = pd.to_datetime(df[col_name], errors='coerce')
    mask = df[col_name].isnull()
    df.loc[mask, col_name] = pd.to_datetime(default_date)
    return df

def standardize_birth_dates(df, col_name="birth_date"):
    df[col_name] = pd.to_datetime(df[col_name], errors='coerce')
    return df