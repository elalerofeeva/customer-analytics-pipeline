import csv
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "shop.db"


def create_tables(connection: sqlite3.Connection) -> None:
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS orders;")
    cursor.execute("DROP TABLE IF EXISTS customers;")

    cursor.execute(
        '''
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            city TEXT NOT NULL,
            segment TEXT NOT NULL
        );
        '''
    )

    cursor.execute(
        '''
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );
        '''
    )

    connection.commit()


def load_csv_to_table(connection: sqlite3.Connection, file_path: Path, table_name: str) -> None:
    with file_path.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    if not rows:
        return

    columns = list(rows[0].keys())
    placeholders = ", ".join(["?"] * len(columns))
    column_names = ", ".join(columns)
    values = [tuple(row[column] for column in columns) for row in rows]

    connection.executemany(
        f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})",
        values
    )
    connection.commit()


def main() -> None:
    connection = sqlite3.connect(DB_PATH)
    create_tables(connection)
    load_csv_to_table(connection, DATA_DIR / "customers.csv", "customers")
    load_csv_to_table(connection, DATA_DIR / "orders.csv", "orders")
    connection.close()

    print(f"База данных создана: {DB_PATH}")


if __name__ == "__main__":
    main()
