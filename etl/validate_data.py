from pathlib import Path

import pandas as pd


RAW_DATA_DIR = Path("data/raw")


def load_csv(filename):
    """Load one generated CSV file."""
    return pd.read_csv(RAW_DATA_DIR / filename)


def main():
    datasets = {
        "regions": load_csv("regions.csv"),
        "customers": load_csv("customers.csv"),
        "products": load_csv("products.csv"),
        "sales_reps": load_csv("sales_reps.csv"),
        "sales": load_csv("sales.csv"),
    }

    print("NEXUS DATA VALIDATION")
    print("=" * 40)

    # 1. Check row counts, columns, and missing values
    for name, df in datasets.items():
        print(f"\nDataset: {name}")
        print(f"Rows: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        print(f"Missing values: {df.isna().sum().sum()}")

    # 2. Check primary-key uniqueness
    primary_keys = {
        "regions": "region_id",
        "customers": "customer_id",
        "products": "product_id",
        "sales_reps": "rep_id",
        "sales": "sale_id",
    }

    print("\nPRIMARY KEY CHECKS")
    for name, key in primary_keys.items():
        df = datasets[name]
        duplicates = df[key].duplicated().sum()
        print(f"{name}.{key}: {duplicates} duplicate values")

    # 3. Check foreign-key references
    customers = datasets["customers"]
    products = datasets["products"]
    regions = datasets["regions"]
    sales_reps = datasets["sales_reps"]
    sales = datasets["sales"]

    checks = {
        "customers.region_id": (
            customers["region_id"],
            set(regions["region_id"]),
        ),
        "sales_reps.region_id": (
            sales_reps["region_id"],
            set(regions["region_id"]),
        ),
        "sales.customer_id": (
            sales["customer_id"],
            set(customers["customer_id"]),
        ),
        "sales.product_id": (
            sales["product_id"],
            set(products["product_id"]),
        ),
        "sales.rep_id": (
            sales["rep_id"],
            set(sales_reps["rep_id"]),
        ),
    }

    print("\nFOREIGN KEY CHECKS")
    for name, (values, valid_ids) in checks.items():
        invalid_count = (~values.isin(valid_ids)).sum()
        print(f"{name}: {invalid_count} invalid references")

    # 4. Check numeric business rules
    print("\nBUSINESS RULE CHECKS")
    print(
        "Non-positive quantities:",
        (sales["quantity"] <= 0).sum(),
    )
    print(
        "Non-positive product prices:",
        (products["price"] <= 0).sum(),
    )
    print(
        "Negative product costs:",
        (products["cost"] < 0).sum(),
    )
    print(
        "Negative transaction prices:",
        (sales["unit_price"] < 0).sum(),
    )

    print("\nValidation report completed.")


if __name__ == "__main__":
    main()