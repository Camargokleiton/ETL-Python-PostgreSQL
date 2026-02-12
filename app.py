import Connetion.conn as conn
import pandas as pd

if __name__ == "__main__":

    connection = conn.connection()

    conn.execute_query(connection, "SET search_path TO public;")

    query = (
        "SELECT * "
        "FROM sensor_data;"
    )

    result = conn.execute_read_query(connection, query)

    result_df = pd.DataFrame(result, columns=['id', 'device_id', 'temp', 'timestamp'])
    print("DataFrame created:")
    print(result_df.head(10))

    # SALVAR NO CSV (do jeito certo)
    result_df.to_csv('Data/DataOutput/sensor_data.csv', index=False)

    conn.close_connection(connection)
