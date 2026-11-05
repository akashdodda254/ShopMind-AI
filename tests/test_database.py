from database.db import (
    initialize_database,
    add_product,
    get_all_products,
    get_product_by_id,
    search_products
)


# Initialize database
initialize_database()


# Insert a sample product
product_id = add_product(
    name="ASUS Vivobook 15",
    brand="ASUS",
    category="Laptop",
    price=55000,
    rating=4.5,
    rating_count=250,
    description="Laptop suitable for programming and college.",
    specifications="16GB RAM, 512GB SSD, Intel Core i5",
    stock=20
)


# Retrieve all products
print("\nALL PRODUCTS:")

products = get_all_products()

for product in products:
    print(product)


# Retrieve product using ID
print("\nPRODUCT BY ID:")

product = get_product_by_id(product_id)

print(product)


# Search products
print("\nSEARCH RESULTS:")

results = search_products(
    category="Laptop",
    max_price=70000,
    min_rating=4.0
)

for result in results:
    print(result)