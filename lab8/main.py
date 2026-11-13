import json
import os

from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order

FILENAME: str = "inventory.json"


# ---------------- Supplier helpers ----------------
def find_supplier(suppliers: list[Supplier], supplier_id: str) -> Supplier | None:
    for supplier in suppliers:
        if supplier.get_supplier_id().lower() == supplier_id.lower():
            return supplier
    return None


def add_supplier(suppliers: list[Supplier]) -> Supplier | None:
    supplier_id = input("New supplier ID: ").strip()
    if not supplier_id:
        print("Supplier ID cannot be empty.")
        return None
    if find_supplier(suppliers, supplier_id) is not None:
        print("A supplier with that ID already exists.")
        return None
    name = input("Supplier name: ").strip()
    contact_email = input("Contact email: ").strip()
    supplier = Supplier(supplier_id, name, contact_email)
    suppliers.append(supplier)
    print("Supplier added.")
    return supplier


def choose_supplier(suppliers: list[Supplier]) -> Supplier | None:
    print("Suppliers:")
    if not suppliers:
        print("  (none yet)")
    for supplier in suppliers:
        supplier.display_information()
    supplier_id = input("Supplier ID (or NEW to add one): ").strip()
    if supplier_id.upper() == "NEW":
        return add_supplier(suppliers)
    supplier = find_supplier(suppliers, supplier_id)
    if supplier is None:
        print("Supplier not found.")
    return supplier


# ---------------- File handling (kept outside the model classes) ----------------
def load_inventory(inventory: Inventory, suppliers: list[Supplier]) -> bool:
    """Read inventory.json: suppliers first, then products that point to them."""
    if not os.path.exists(FILENAME):
        return False
    try:
        with open(FILENAME, "r") as file:
            data = json.load(file)

        for item in data["suppliers"]:
            suppliers.append(
                Supplier(item["supplier_id"], item["name"], item["contact_email"])
            )

        for item in data["products"]:
            supplier = find_supplier(suppliers, item["supplier_id"])
            if supplier is None:
                print(f"Skipping '{item['product_id']}': unknown supplier.")
                continue
            product_type = item.get("type")
            if product_type == "physical":
                product = PhysicalProduct(
                    item["product_id"], item["name"], item["price"],
                    item["stock"], supplier, item["weight"]
                )
            elif product_type == "digital":
                product = DigitalProduct(
                    item["product_id"], item["name"], item["price"],
                    item["stock"], supplier, item["download_size"]
                )
            else:
                print(f"Skipping '{item.get('product_id')}': unknown product type.")
                continue
            inventory.add_product(product)
        return True
    except (json.JSONDecodeError, KeyError, TypeError):
        print("Could not read inventory.json - starting with sample data.")
        return False


def save_inventory(inventory: Inventory, suppliers: list[Supplier]) -> None:
    """Save suppliers and products. Each product stores its supplier's ID."""
    # Include every supplier in the list AND any supplier a product points to,
    # so the saved file is always complete.
    all_suppliers: list[Supplier] = list(suppliers)
    for product in inventory.get_products():
        if find_supplier(all_suppliers, product.get_supplier().get_supplier_id()) is None:
            all_suppliers.append(product.get_supplier())

    supplier_data: list[dict] = []
    for supplier in all_suppliers:
        supplier_data.append({
            "supplier_id": supplier.get_supplier_id(),
            "name": supplier.get_name(),
            "contact_email": supplier.get_contact_email(),
        })

    product_data: list[dict] = []
    for product in inventory.get_products():
        item = {
            "product_id": product.get_product_id(),
            "type": "",
            "name": product.get_name(),
            "price": product.get_price(),
            "stock": product.get_stock(),
            "supplier_id": product.get_supplier().get_supplier_id(),
        }
        if isinstance(product, PhysicalProduct):
            item["type"] = "physical"
            item["weight"] = product.get_weight()
        elif isinstance(product, DigitalProduct):
            item["type"] = "digital"
            item["download_size"] = product.get_download_size()
        product_data.append(item)

    with open(FILENAME, "w") as file:
        json.dump({"suppliers": supplier_data, "products": product_data}, file, indent=4)
    print("Inventory saved.")


# ---------------- Menu actions ----------------
def add_product_action(inventory: Inventory, suppliers: list[Supplier]) -> None:
    print("Product type:")
    print("1. Physical product")
    print("2. Digital product")
    type_choice = input("Choose type (1-2): ").strip()
    if type_choice not in ("1", "2"):
        print("Invalid product type.")
        return

    supplier = choose_supplier(suppliers)
    if supplier is None:
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
        product = PhysicalProduct(product_id, name, price, stock, supplier, extra)
    else:
        product = DigitalProduct(product_id, name, price, stock, supplier, extra)

    if inventory.add_product(product):
        print("Product added.")
    else:
        print("A product with that ID already exists.")


def update_stock_action(inventory: Inventory) -> None:
    product_id = input("Product ID to update: ").strip()
    product = inventory.find_product(product_id)
    if product is None:
        print("Product not found.")
        return
    try:
        quantity = int(input("New stock quantity: "))
        product.update_stock(quantity)  # Product decides if the value is OK
        print("Stock updated.")
    except ValueError as error:
        print(f"Invalid input: {error}")


def search_action(inventory: Inventory) -> None:
    keyword = input("Search by ID or name: ").strip()
    results = inventory.search_product(keyword)
    if not results:
        print("No matching products.")
        return
    for product in results:
        product.display_information()


def remove_product_action(inventory: Inventory) -> None:
    product_id = input("Product ID to remove: ").strip()
    if inventory.remove_product(product_id):
        print("Product removed from the inventory.")
    else:
        print("Product not found.")


def create_order_action(inventory: Inventory) -> None:
    order = Order(input("Order ID: ").strip())
    while True:
        product_id = input("Product ID to add (press Enter to finish): ").strip()
        if product_id == "":
            break
        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue
        try:
            quantity = int(input("Quantity: "))
        except ValueError:
            print("Quantity must be a whole number.")
            continue
        try:
            order.add_order_line(product, quantity)  # the Order creates the line
            print("Added to order.")
        except ValueError as error:
            print(f"Invalid input: {error}")

    if not order.get_order_lines():
        print("Order cancelled - no items were added.")
        return
    print()
    order.display_information()


def print_menu() -> None:
    print("\n=== Inventory Management System ===")
    print("1. Display all products")
    print("2. Add a product")
    print("3. Update stock")
    print("4. Search for a product")
    print("5. Remove a product")
    print("6. Create an order")
    print("7. Save inventory")
    print("8. Exit")


def load_sample_data(inventory: Inventory, suppliers: list[Supplier]) -> None:
    techsource = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.com")
    softworks = Supplier("S002", "SoftWorks Studio", "hello@softworks.com")
    suppliers.append(techsource)
    suppliers.append(softworks)
    inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, techsource, 2.5))
    inventory.add_product(DigitalProduct("D001", "Photo Editor", 49.99, 100, softworks, 450.0))


def main() -> None:
    inventory = Inventory()
    suppliers: list[Supplier] = []

    if not load_inventory(inventory, suppliers):
        inventory = Inventory()  # start clean if loading failed part-way
        suppliers = []
        load_sample_data(inventory, suppliers)

    while True:
        print_menu()
        choice = input("Choose an option (1-8): ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product_action(inventory, suppliers)
        elif choice == "3":
            update_stock_action(inventory)
        elif choice == "4":
            search_action(inventory)
        elif choice == "5":
            remove_product_action(inventory)
        elif choice == "6":
            create_order_action(inventory)
        elif choice == "7":
            save_inventory(inventory, suppliers)
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
