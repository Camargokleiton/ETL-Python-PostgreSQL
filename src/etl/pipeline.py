from logging import config
import os
import transform.cleaning as dt
import load.load as sf
import extract.extract as extract
import logging as log

log.basicConfig(level=log.INFO)

def run_pipeline():
    df_customers = extract.create_dataframe("customers")
    df_orders = extract.create_dataframe("orders")  

    df_customers.columns = [
        'customer_id','name', 'email', 'phone',
        'birth_date', 'created_at','is_active'
    ]

    df_orders.columns = [
        'order_id', 'customer_id', 'order_date',
        'status', 'amount','payment_method', 'created_at'
    ]

    # Remove duplicates
    df_customers = dt.remove_duplicates(df_customers, subset_cols=["customer_id"])
    df_orders = dt.remove_duplicates(df_orders, subset_cols=["order_id"])

    # Data cleaning
    df_orders = dt.fill_missing_order_dates(df_orders)
    df_customers = dt.fill_missing_emails(df_customers)
    df_customers = dt.fill_missing_phones(df_customers)
    df_customers = dt.fill_invalid_birth_dates(df_customers)
    df_orders = dt.fill_missing_status(df_orders)
    df_orders = dt.convert_amount_to_float(df_orders)
    df_orders = dt.fill_negative_amounts(df_orders)

    # Standardization
    df_customers['phone'] = df_customers['phone'].apply(dt.normalize_phone)
    df_customers = dt.standardize_birth_dates(df_customers)
    df_orders = dt.standardize_payment_methods(df_orders)

    # Output
    
    output_path = os.getenv("OUTPUT_PATH", "data/output")
    file_path_customers = os.path.join(output_path, "customers.csv")
    file_path_orders = os.path.join(output_path, "orders.csv")
    
    sf.save_to_csv(df_customers, file_path_customers)
    sf.save_to_csv(df_orders, file_path_orders)

    log.info("ETL pipeline finished successfully.")


if __name__ == "__main__":
    run_pipeline()



