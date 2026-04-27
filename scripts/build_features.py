from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_PATH = DATA_DIR / "customer_features.csv"


def build_customer_features(orders_df: pd.DataFrame, customers_df: pd.DataFrame) -> pd.DataFrame:
    """Build an aggregated customer feature table from paid orders."""


def build_customer_features(orders_df: pd.DataFrame, customers_df: pd.DataFrame) -> pd.DataFrame:
    paid_orders = orders_df[orders_df["status"] == "paid"].copy()

    merged = paid_orders.merge(customers_df, on="customer_id", how="left")

    features = (
        merged.groupby(["customer_id", "name", "city", "segment"])
        .agg(
            total_spent=("amount", "sum"),
            orders_count=("order_id", "count"),
            avg_check=("amount", "mean"),
            last_order_date=("order_date", "max")
        )
        .reset_index()
    )

    features["value_segment"] = np.where(
        features["total_spent"] >= 5000,
        "VIP",
        "Regular"
    )

    features["avg_check"] = features["avg_check"].round(2)
    features["total_spent"] = features["total_spent"].round(2)

    return features


def main() -> None:
    orders_df = pd.read_csv(DATA_DIR / "orders.csv")
    customers_df = pd.read_csv(DATA_DIR / "customers.csv")

    features_df = build_customer_features(orders_df, customers_df)
    features_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")

    print("Клиентская витрина сохранена в файл:")
    print(OUTPUT_PATH)
    print("\nПервые строки результата:")
    print(features_df.head())


if __name__ == "__main__":
    main()
