
from DataTratament.tratament import normalize_phone
from DataTratament.tratament import fill_missing_emails, fill_missing_phones
from DataTratament.tratament import fill_missing_order_dates, fill_invalid_birth_dates
from DataTratament.tratament import fill_missing_status, convert_amount_to_float
from DataTratament.tratament import fill_negative_amounts, standardize_birth_dates
from DataTratament.tratament import standardize_payment_methods, remove_duplicates

import pandas as pd


def test_normalize_phone_valid():
    assert normalize_phone("41999998888") == "5541999998888"


def test_normalize_phone_with_symbols():
    assert normalize_phone("(41) 99999-8888") == "5541999998888"


def test_normalize_phone_invalid():
    assert normalize_phone("123") is None


def test_normalize_phone_null():
    assert normalize_phone(None) is None

    
def test_fill_missing_emails():
    data = {
        'name': ['Ana Silva', 'João Souza', 'Maria Oliveira'],
        'email': [None, 'joaosouza@email.com', None]}

    df = pd.DataFrame(data)
    df_filled = fill_missing_emails(df)
    assert df_filled['email'].iloc[0] == 'anasilva@email.com'
    assert df_filled['email'].iloc[2] == 'mariaoliveira@email.com'
    
def test_fill_missing_phones():
    data = {
        'name': ['Ana Silva', 'João Souza', 'Maria Oliveira'],
        'phone': [None, '41999998888', None]}

    df = pd.DataFrame(data)
    df_filled = fill_missing_phones(df)
    assert df_filled['phone'].iloc[0] == "5541900000000"
    assert df_filled['phone'].iloc[2] == "5541900000000"

def test_fill_invalid_birth_dates():
    data = {
        'name': ['Ana Silva', 'João Souza', 'Maria Oliveira'],
        'birth_date': ['1990-01-01', 'invalid_date', None]
    }

    df = pd.DataFrame(data)
    df_filled = fill_invalid_birth_dates(df)

    assert df_filled['birth_date'].iloc[1] == pd.Timestamp("1990-01-01")
    assert df_filled['birth_date'].iloc[2] == pd.Timestamp("1990-01-01")


def test_fill_missing_order_dates():
    data = {
        'order_id': [1, 2, 3],
        'order_date': ['2023-01-01', None, '2023-01-03']
    }

    df = pd.DataFrame(data)
    df_filled = fill_missing_order_dates(df, default_date="2023-01-02")

    assert df_filled['order_date'].iloc[1] == pd.Timestamp("2023-01-02")


def test_fill_missing_status():
    data = {
        'order_id': [1, 2, 3],
        'status': ['completed', None, 'pending']}

    df = pd.DataFrame(data)
    df_filled = fill_missing_status(df)
    assert df_filled['status'].iloc[1] == "pending"

def test_convert_amount_to_float():
    data = {
        'order_id': [1, 2, 3],
        'amount': ['100.50', 'invalid_amount', None]}

    df = pd.DataFrame(data)
    df_converted = convert_amount_to_float(df)
    assert df_converted['amount'].iloc[0] == 100.50
    assert pd.isna(df_converted['amount'].iloc[1])
    assert pd.isna(df_converted['amount'].iloc[2])

def test_fill_negative_amounts():
    data = {
        'order_id': [1, 2, 3],
        'amount': [100.50, -50.00, None]}

    df = pd.DataFrame(data)
    df_filled = fill_negative_amounts(df)
    assert df_filled['amount'].iloc[1] == 0.0
    assert pd.isna(df_filled['amount'].iloc[2])

def test_standardize_birth_dates():
    data = {
        'name': ['Ana Silva', 'João Souza', 'Maria Oliveira'],
        'birth_date': ['01/01/1990', '1990-01-01', '1990.01.01']
    }

    df = pd.DataFrame(data)
    df_standardized = standardize_birth_dates(df)

    assert df_standardized['birth_date'].iloc[0] == "1990-01-01"
    



def test_standardize_payment_methods():
    data = {
        'order_id': [1, 2, 3, 4],
        'payment_method': ['Credit Card', 'debit card', 'PayPal', 'unknown method']}

    df = pd.DataFrame(data)
    df_standardized = standardize_payment_methods(df)
    assert df_standardized['payment_method'].iloc[0] == "credit_card"
    assert df_standardized['payment_method'].iloc[1] == "debit_card"
    assert df_standardized['payment_method'].iloc[2] == "paypal"
    assert df_standardized['payment_method'].iloc[3] == "other"

def test_remove_duplicates():
    data = {
        'customer_id': [1, 2, 2, 3],
        'name': ['Ana Silva', 'João Souza', 'João Souza', 'Maria Oliveira']}

    df = pd.DataFrame(data)
    df_no_duplicates = remove_duplicates(df, subset_cols=["customer_id"])
    assert len(df_no_duplicates) == 3
    assert df_no_duplicates['customer_id'].iloc[0] == 1
    assert df_no_duplicates['customer_id'].iloc[1] == 2
    assert df_no_duplicates['customer_id'].iloc[2] == 3


    