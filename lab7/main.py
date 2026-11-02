import json
import os

from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory

FILENAME = "inventory.json"


# ---------------- File handling (kept outside the Product classes) ----------------
def load_inventory(inventory):
    """Read inventory.json. The "type" field tells us which class to create."""
    if not os.path.exists(FILENAME):
        return False
    try:
        with open(FILENAME, "r") as file:
            data = json.load(file)
        for item in data:
            product_type = item.get("type")
            if product_type == "physical":
                product = PhysicalProduct(
                    item["product_id"], item["name"], item["price"],
                    item["stock"], item["weight"]
                )
            elif product_type == "digital":
                product = DigitalProduct(
                    item["product_id"], item["name"], item["price"],
                    item["stock"], item["download_size"]
                )
            else:
                print(f"Skipping '{item.get('product_id')}': unknown product type.")
                continue
            inventory.add_product(product)
        return True
    except (json.JSONDecodeError, KeyError):
        print("Could not read inventory.json - starting with sample products.")
        return False


def save_inventory(inventory):
    """Turn each Product object into a dictionary (with its type) and save."""
    data = []
    for product in inventory.get_products():
        item = {
            "product_id": product.get_product_id(),
            "type": "",
            "name": product.get_name(),
            "price": product.get_price(),
            "stock": product.get_stock(),
        }
        if isinstance(product, PhysicalProduct):
            item["type"] = "physical"
            item["weight"] = product.get_weight()
        elif isinstance(product, DigitalProduct):
            item["type"] = "digital"
            item["download_size"] = product.get_download_size()
        data.append(item)
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)
    print("Inventory saved.")


# ---------------- Menu actions: get input, call Inventory/Product methods ----------------
def add_product_action(inventory):
    print("Product type:")
    print("1. Physical product")
    print("2. Digital product")
    type_choice = input("Choose type (1-2): ").strip()
    if type_choice not in ("1", "2"):
        print("Invalid product type.")
        return

    product_id = input("Product ID: ").strip()
    name = input("Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock: "))
        if type_choice == "1":
            extra = float(input("Weight (kg): "))
        else:
            extra = float(input("Download size (MB): "))
    except ValueError:
        print("Price, weight and size must be numbers, and stock must be a whole number.")
        return
    if price < 0 or stock < 0 or extra < 0:
        print("Values cannot be negative.")
        return

    if type_choice == "1":
        product = PhysicalProduct(product_id, name, price, stock, extra)
    else:
        product = DigitalProduct(product_id, name, price, stock, extra)

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

    # Load saved data; if there is none, start with sample products of both types
    if not load_inventory(inventory):
        inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.5))
        inventory.add_product(DigitalProduct("D001", "Photo Editor", 49.99, 100, 450.0))

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
