"""
ShopMind - Product Dataset Loader

Loads products from CSV into the SQLite database.
"""

import pandas as pd

from database.db import (
    initialize_database,
    add_products,
    get_all_products
)

from pathlib import Path


# --------------------------------------------------
# FILE CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_PATH = BASE_DIR / "data" / "products.csv"


# --------------------------------------------------
# LOAD CSV DATA
# --------------------------------------------------

def load_csv_data():

    if not CSV_PATH.exists():

        raise FileNotFoundError(
            f"Product dataset not found: {CSV_PATH}"
        )

    dataframe = pd.read_csv(CSV_PATH)

    print(f"Loaded {len(dataframe)} products from CSV.")

    return dataframe


# --------------------------------------------------
# VALIDATE DATA
# --------------------------------------------------

def validate_data(dataframe):

    required_columns = [
        "name",
        "brand",
        "category",
        "price",
        "rating",
        "rating_count",
        "description",
        "specifications",
        "stock"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:

        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    if dataframe[required_columns].isnull().any().any():

        raise ValueError(
            "Dataset contains missing values."
        )

    if dataframe["price"].lt(0).any():

        raise ValueError("Product prices cannot be negative.")

    if not dataframe["rating"].between(0, 5).all():

        raise ValueError("Ratings must be between 0 and 5.")

    if dataframe["rating_count"].lt(0).any():

        raise ValueError("Rating counts cannot be negative.")

    if dataframe["stock"].lt(0).any():

        raise ValueError("Stock cannot be negative.")

    if dataframe["name"].duplicated().any():

        raise ValueError("Duplicate product names detected.")

    print("Dataset validation successful!")


# --------------------------------------------------
# INSERT PRODUCTS
# --------------------------------------------------

def insert_products(dataframe):

    products = dataframe.to_dict(orient="records")

    total_inserted = add_products(products)

    print(f"Successfully inserted {total_inserted} products.")


# --------------------------------------------------
# DISPLAY DATABASE SUMMARY
# --------------------------------------------------

def display_summary():

    products = get_all_products()

    print("\n========== SHOPMIND DATABASE SUMMARY ==========")

    print(f"Total products: {len(products)}")

    categories = {}

    for product in products:

        category = product["category"]

        categories[category] = categories.get(category, 0) + 1

    print("\nProducts by category:")

    for category, count in categories.items():

        print(f"{category}: {count}")

    print("===============================================")


# --------------------------------------------------
# MAIN EXECUTION
# --------------------------------------------------

def main():

    print("\nInitializing ShopMind product database...\n")

    initialize_database()

    dataframe = load_csv_data()

    validate_data(dataframe)

    insert_products(dataframe)

    display_summary()


if __name__ == "__main__":

    main()