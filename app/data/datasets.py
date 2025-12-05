import os
import pandas as pd

def load_csv_to_table(conn, csv_path, table_name):
    # 1. Check if file exists
    if not os.path.exists(csv_path):
        print(f"CSV file not found: {csv_path}")
        return 0

    # 2. Load CSV into DataFrame
    df = pd.read_csv(csv_path)

    # 3. Insert data into SQL table
    df.to_sql(name=table_name, con=conn, if_exists='append', index=False)

    # 4. Show result
    row_count = len(df)
    print(f"Loaded {row_count} rows into '{table_name}'")

    return row_count

def load_all_csv_data(conn):
    """
    Loads every domain CSV required by the platform.
    Update the paths to match your folder structure.
    """
    total_rows = 0

    csv_files = {
        "cyber_incidents": "DATA/cyber_incidents.csv",
        "datasets_metadata": "DATA/datasets_metadata.csv",
        "it_tickets": "DATA/it_tickets.csv"
    }

    for table, path in csv_files.items():
        print(f" - Loading {path} into {table}")
        total_rows += load_csv_to_table(conn, path, table)

    print(f"\nTotal CSV rows loaded: {total_rows}")
    return total_rows