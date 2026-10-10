from pathlib import Path

import numpy as np
import pandas as pd


# Configuration
RANDOM_SEED = 42

NUM_CUSTOMERS = 500
NUM_PRODUCTS = 50
NUM_SALES_REPS = 30
NUM_SALES = 5000

RAW_DATA_DIR = Path("data/raw")

# Reproducible random data
rng = np.random.default_rng(RANDOM_SEED)

# Create the output directory if it does not exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


# 1. Regions
regions = pd.DataFrame({
    "region_id": ["R01", "R02", "R03", "R04"],
    "region_name": ["North", "South", "East", "West"],
})


# 2. Products
products = pd.DataFrame({
    "product_id": [f"P{i:03d}" for i in range(1, NUM_PRODUCTS + 1)],
    "category": rng.choice(
        ["Industrial", "Consumer", "Electronics", "Components"],
        size=NUM_PRODUCTS,
    ),
})

products["cost"] = rng.uniform(5000, 80000, size=NUM_PRODUCTS).round(2)
products["price"] = (
    products["cost"] * rng.uniform(1.25, 1.75, size=NUM_PRODUCTS)
).round(2)

products = products[["product_id", "category", "price", "cost"]]


# 3. Customers
customers = pd.DataFrame({
    "customer_id": [f"C{i:04d}" for i in range(1, NUM_CUSTOMERS + 1)],
    "segment": rng.choice(
        ["Enterprise", "Mid-Market", "SMB"],
        size=NUM_CUSTOMERS,
        p=[0.25, 0.35, 0.40],
    ),
    "region_id": rng.choice(regions["region_id"], size=NUM_CUSTOMERS),
    "join_date": rng.choice(
        pd.date_range("2022-01-01", "2026-01-01"),
        size=NUM_CUSTOMERS,
    ),
    "status": rng.choice(
        ["Active", "Inactive"],
        size=NUM_CUSTOMERS,
        p=[0.90, 0.10],
    ),
})


# 4. Sales representatives
sales_reps = pd.DataFrame({
    "rep_id": [f"REP{i:03d}" for i in range(1, NUM_SALES_REPS + 1)],
    "region_id": rng.choice(regions["region_id"], size=NUM_SALES_REPS),
    "hire_date": rng.choice(
        pd.date_range("2022-01-01", "2025-12-31"),
        size=NUM_SALES_REPS,
    ),
})

# Ensure every region has at least one sales representative
for region_id in regions["region_id"]:
    if region_id not in sales_reps["region_id"].values:
        sales_reps.loc[len(sales_reps) - 1, "region_id"] = region_id


# 5. Sales transactions
sales = pd.DataFrame({
    "sale_id": [f"S{i:06d}" for i in range(1, NUM_SALES + 1)],
    "customer_id": rng.choice(customers["customer_id"], size=NUM_SALES),
    "product_id": rng.choice(products["product_id"], size=NUM_SALES),
    "sale_date": rng.choice(
        pd.date_range("2025-01-01", "2026-09-30"),
        size=NUM_SALES,
    ),
    "quantity": rng.integers(1, 50, size=NUM_SALES),
})

# Assign each sale a representative from the customer's region
customer_regions = customers.set_index("customer_id")["region_id"]
sales["customer_region"] = sales["customer_id"].map(customer_regions)

reps_by_region = {
    region_id: sales_reps.loc[
        sales_reps["region_id"] == region_id, "rep_id"
    ].tolist()
    for region_id in regions["region_id"]
}

sales["rep_id"] = sales["customer_region"].map(
    lambda region_id: rng.choice(reps_by_region[region_id])
)

# Apply a transaction-specific discount to the product's list price
product_prices = products.set_index("product_id")["price"]
sales["list_price"] = sales["product_id"].map(product_prices)
discounts = rng.uniform(0.00, 0.15, size=NUM_SALES)

sales["unit_price"] = (sales["list_price"] * (1 - discounts)).round(2)

sales = sales[
    [
        "sale_id",
        "customer_id",
        "product_id",
        "rep_id",
        "sale_date",
        "quantity",
        "unit_price",
    ]
]


# Save CSV files
datasets = {
    "regions": regions,
    "customers": customers,
    "products": products,
    "sales_reps": sales_reps,
    "sales": sales,
}

for name, dataframe in datasets.items():
    dataframe.to_csv(RAW_DATA_DIR / f"{name}.csv", index=False)
    print(f"Created {name}.csv: {len(dataframe)} rows")

print(f"\nAll raw datasets saved to: {RAW_DATA_DIR.resolve()}")