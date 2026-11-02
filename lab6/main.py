import json
import os

from product import Product
from inventory import Inventory

FILENAME = "inventory.json"


# ---------------- File handling (kept outside Product and Inventory) ----------------
def load_inventory(inventory):
    """Read inventory.json and turn each dictionary into a Product object."""
    if not os.path.exists(FILENAME):
        return False
    try:
        with open(FILENAME, "r") as file:
            data = json.load(file)
        for item in data:
            product = Product(
                item["product_id"], item["name"], item["price"], item["stock"]
            )
            inventory.add_product(product)
        return True
    except (json.JSONDecodeError, KeyError):
        print("Could not read inventory.json - starting with an empty inventory.")
        return False


def save_inventory(inventory):
    """Turn each Product object back into a dictionary and write to JSON."""
    data = []
    for product in inventory.get_products():
        data.append({
            "product_id": product.get_product_id(),
            "name": product.get_name(),
            "price": product.get_price(),
            "stock": product.get_stock(),
        })
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)
    print("Inventory saved.")


# ---------------- Menu actions: get input, call Inventory/Product methods ----------------
def add_product_action(inventory):
    product_id = input("Product ID: ").strip()
    name = input("Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock: "))
    except ValueError:
        print("Price must be a number and stock must be a whole number.")
        return
    if price < 0 or stock < 0:
        print("Price and stock cannot be negative.")
        return

    product = Product(product_id, name, price, stock)
    if inventory.add_product(product):
        print("Product added.")
    else:
        print("A product with that ID already exists.")


def update_stock_action(inventory):
    product_id = input("Product ID to update: ").strip()
    product = inventory.get_product(product_id)
    if product is None:
        print("Product not found.")
        return
    try:
        quantity = int(input("New stock quantity: "))
        product.update_stock(quantity)  # Product decides if the value is OK
        print("Stock updated.")
    except ValueError as error:
        print(f"Invalid input: {error}")


def search_action(inventory):
    keyword = input("Search by ID or name: ").strip()
    results = inventory.search_product(keyword)
    if not results:
        print("No matching products.")
        return
    for product in results:
        product.display_information()


def print_menu():
    print("\n=== Inventory Management System ===")
    print("1. Display all products")
    print("2. Add a product")
    print("3. Update stock")
    print("4. Search for a product")
    print("5. Save inventory")
    print("6. Exit")


def main():
    inventory = Inventory()

    # Load saved data; if there is none, start with two sample products
    if not load_inventory(inventory):
        inventory.add_product(Product("P001", "Laptop", 1200.00, 15))
        inventory.add_product(Product("P002", "Mouse", 25.50, 40))

    while True:
        print_menu()
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product_action(inventory)
        elif choice == "3":
            update_stock_action(inventory)
        elif choice == "4":
            search_action(inventory)
        elif choice == "5":
            save_inventory(inventory)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
