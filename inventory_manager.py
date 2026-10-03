import json
import os


def load_inventory():
    if os.path.exists("inventory.json"):
        try:
            with open("inventory.json", "r") as file:
                inventory = json.load(file)

            print("inventory.json found.")
            print("Inventory loaded successfully.")
            return inventory

        except json.JSONDecodeError:
            print("Error: inventory.json is invalid.")
            return []

    else:
        print("inventory.json not found.")
        print("Starting with an empty inventory.")
        return []


def save_inventory(inventory):
    with open("inventory.json", "w") as file:
        json.dump(inventory, file, indent=4)

    print("Inventory saved successfully to inventory.json.")


def display_all(inventory):
    print("\nCurrent Inventory")
    print("------------------------------------------------")

    if not inventory:
        print("No products found.")

    else:
        for product in inventory:
            print(
                f"ID: {product['id']} | "
                f"Name: {product['name']} | "
                f"Price: ${product['price']:.2f} | "
                f"Stock: {product['stock']}"
            )

    print("------------------------------------------------")


def add_product(inventory):
    print("\nAdd New Product")

    product_id = input("Product ID: ").strip()

    for product in inventory:
        if product["id"].lower() == product_id.lower():
            print("Error: Product ID already exists.")
            return

    product_name = input("Product Name: ").strip()

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))

        if price < 0 or stock < 0:
            print("Error: Price and stock cannot be negative.")
            return

    except ValueError:
        print("Error: Please enter a valid price and stock quantity.")
        return

    product = {
        "id": product_id,
        "name": product_name,
        "price": price,
        "stock": stock
    }

    inventory.append(product)

    print("Product added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")

    product_id = input("Enter Product ID: ").strip()

    for product in inventory:
        if product["id"].lower() == product_id.lower():

            print("Product Found:")
            print("Name:", product["name"])
            print("Current Stock:", product["stock"])

            try:
                new_stock = int(input("New Stock Quantity: "))

                if new_stock < 0:
                    print("Error: Stock cannot be negative.")
                    return

                product["stock"] = new_stock
                print("Stock updated successfully!")

            except ValueError:
                print("Error: Please enter a valid stock quantity.")

            return

    print("Product not found.")


def search_product(inventory):
    print("\nSearch Product")

    product_id = input("Enter Product ID: ").strip()

    for product in inventory:
        if product["id"].lower() == product_id.lower():

            print("Product Found")
            print("------------------------------------------------")
            print("ID:", product["id"])
            print("Name:", product["name"])
            print(f"Price: ${product['price']:.2f}")
            print("Stock:", product["stock"])
            print("------------------------------------------------")

            return

    print("Product not found.")


def main():
    inventory = load_inventory()

    while True:

        print("\n========================================")
        print("INVENTORY MANAGEMENT SYSTEM")
        print("========================================")
        print("----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("----------------------------")

        option = input("Enter option: ").strip()

        if option == "1":
            display_all(inventory)

        elif option == "2":
            add_product(inventory)

        elif option == "3":
            update_stock(inventory)

        elif option == "4":
            search_product(inventory)

        elif option == "5":
            print("Saving inventory...")
            save_inventory(inventory)

        elif option == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break

        else:
            print("Invalid option. Please enter a number from 1 to 6.")


main()