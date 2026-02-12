import DataTratament.tratament as dt
import DataTratament.saveFile as sf
import DataTratament.ingest as ingest


if __name__ == "__main__":

    df_customers = ingest.create_dataframe("customers")
    df_orders = ingest.create_dataframe("orders")  
    
    
    
    df_customers.columns = ['customer_id','name', 'email', 'phone', 'birth_date', 'created_at','is_active']
    df_orders.columns = ['order_id', 'customer_id', 'order_date', 'status', 'amount','payment_method', 'created_at']

    # Remove duplicates
    df_customers = dt.remove_duplicate(df_customers, subset_cols=["customer_id"])
    df_orders = dt.remove_duplicate(df_orders, subset_cols=["order_id"])
    
    
    # fill missing and invalid data
    df_orders = dt.fill_missing_order_dates(df_orders) # fill missing order dates with default date
    df_customers = dt.fill_missing_emails(df_customers) # fill missing emails
    df_customers = dt.fill_missing_phones(df_customers) # fill missing phones with default number
    df_customers = dt.fill_invalid_birth_dates(df_customers) # fill invalid birth dates with default date
    df_orders = dt.fill_missing_status(df_orders) # fill missing status with 'pending'
    df_orders = dt.convert_amount_to_float(df_orders) # convert amount to float
    df_orders = dt.fill_negative_amounts(df_orders) # fill negative amounts with 0.0
    
 
    df_customers['phone'] = df_customers['phone'].apply(dt.normalize_phone) # normalize phone numbers
    df_customers = dt.standardize_birth_dates(df_customers) # standardize birth dates
    df_orders = dt.standardize_payment_methods(df_orders) # standardize payment methods
    
    
    
    
    print(df_customers['birth_date'].sort_values())


    sf.save_to_csv(df_customers, "Data/DataOutput/customers.csv")
    sf.save_to_csv(df_orders, "Data/DataOutput/orders.csv")


