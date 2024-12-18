import psycopg2
import pandas as pd
import os

# configuration
DATABASE_CONFIG = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'host.docker.internal',
    'port': 5432
}

CSV_FILE_PATH = './data/processed/processed_stocks.csv'
TABLE_NAME = 'stocks_top_50'

def create_table(df,table_name, cursor):
    sql_types = {
        'object': 'TEXT',
        'int64': 'INTEGER',
        'float64': 'REAL',
        'datetime64[ns]': 'TIMESTAMP',
        'bool': 'BOOLEAN'
    }

    columns = []
    for column,dtype in df.dtypes.items():
        pg_type = sql_types.get(str(dtype),'TEXT')
        columns.append(f"{column} {pg_type}")

    create_table_query = f"""
        drop table if exists {table_name};
        create table {table_name} (
        {', '.join(columns)}
        );
    """

    cursor.execute(create_table_query)
    print(f"table {table_name} created.")


def load_csv_to_postgresql(csv_file,table_name,db_config):
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        df = pd.read_csv(csv_file)
        create_table(df,table_name,cursor)
        columns = ', '.join(df.columns)
        values  = ', '.join(['%s' for _ in df.columns])
        insert_query = f"insert into {table_name} ({columns}) values ({values})"

        data = [tuple(row) for row in df.itertuples(index=False)]

        cursor.executemany(insert_query,data)
        connection.commit()
        print(f"insert into {table_name} complete.")

    except Exception as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        


if __name__ == '__main__':
    load_csv_to_postgresql(CSV_FILE_PATH,TABLE_NAME,DATABASE_CONFIG)