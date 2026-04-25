import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent.parent / "shop.db"


def run_query(connection: sqlite3.Connection, title: str, query: str) -> None:
    print(f"\n=== {title} ===")
    cursor = connection.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def main() -> None:
    if not DB_PATH.exists():
        print("Файл shop.db не найден. Сначала запустите scripts/init_db.py")
        return

    connection = sqlite3.connect(DB_PATH)

    run_query(
        connection,
        "SELECT: все клиенты",
        "SELECT * FROM customers;"
    )

    run_query(
        connection,
        "WHERE: оплаченные заказы дороже 1500",
        '''
        SELECT *
        FROM orders
        WHERE status = 'paid' AND amount > 1500;
        '''
    )

    run_query(
        connection,
        "JOIN: клиенты и заказы",
        '''
        SELECT customers.name,
               customers.city,
               customers.segment,
               orders.order_date,
               orders.amount,
               orders.category,
               orders.status
        FROM customers
        JOIN orders ON customers.customer_id = orders.customer_id;
        '''
    )

    run_query(
        connection,
        "GROUP BY: агрегирование по категориям",
        '''
        SELECT category,
               COUNT(*) AS total_orders,
               ROUND(AVG(amount), 2) AS avg_amount,
               ROUND(SUM(amount), 2) AS total_revenue
        FROM orders
        WHERE status = 'paid'
        GROUP BY category;
        '''
    )

    connection.close()


if __name__ == "__main__":
    main()
