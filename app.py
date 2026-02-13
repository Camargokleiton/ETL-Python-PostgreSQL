import DataTratament.tratament as dt
import DataTratament.saveFile as sf
import DataTratament.ingest as ingest
import logging as log

log.basicConfig(level=log.INFO)

def main():
    df_customers = ingest.create_dataframe("customers")
    df_orders = ingest.create_dataframe("orders")  

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
    sf.save_to_csv(df_customers, "Data/DataOutput/customers.csv")
    sf.save_to_csv(df_orders, "Data/DataOutput/orders.csv")

    log.info("ETL pipeline finished successfully.")


if __name__ == "__main__":
    main()



