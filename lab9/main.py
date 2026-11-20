import json
import os

from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product_factory import ProductFactory
from product_loader import load_products
from inventory import Inventory
from order import Order
from discount_strategy import (DiscountStrategy, NoDiscount, PercentageDiscount,
                               BulkDiscount, StudentDiscount)
from input_helpers import (get_positive_float, get_non_negative_float,
                           get_non_negative_int)

FILENAME: str = "inventory.json"
PRODUCT_TYPES: dict[str, str] = {"1": "physical", "2": "digital"}
DETAIL_PROMPTS: dict[str, str] = {"physical": "Weight (kg): ", "digital": "Download size (MB): "}


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


# ---------------- File handling (JSON) ----------------
def load_inventory(inventory: Inventory, suppliers: list[Supplier]) -> bool:
    """Read inventory.json. Products are built by the ProductFactory."""
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
            detail = item.get("weight", item.get("download_size", 0.0))
            try:
                product = ProductFactory.create(
                    item["type"], item["product_id"], item["name"],
                    item["price"], item["stock"], supplier, detail)
            except ValueError as error:
                print(f"Skipping '{item['product_id']}': {error}")
                continue
            inventory.add_product(product)
        return True
    except (json.JSONDecodeError, KeyError, TypeError):
        print("Could not read inventory.json - starting with sample data.")
        return False


def save_inventory(inventory: Inventory, suppliers: list[Supplier]) -> None:
    """Save suppliers and products. Each product stores its supplier's ID."""
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
    product_type = PRODUCT_TYPES.get(input("Choose type (1-2): ").strip())
    if product_type is None:
        print("Invalid product type.")
        return

    supplier = choose_supplier(suppliers)
    if supplier is None:
        return

    product_id = input("Product ID: ").strip()
    name = input("Name: ").strip()
    price = get_positive_float("Price: ")
    stock = get_non_negative_int("Stock: ")
    detail = get_non_negative_float(DETAIL_PROMPTS[product_type])

    try:
        product = ProductFactory.create(product_type, product_id, name,
                                        price, stock, supplier, detail)
    except ValueError as error:
        print(f"Could not add product: {error}")
        return

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
    quantity = get_non_negative_int("New stock quantity: ")
    product.update_stock(quantity)
    print("Stock updated.")


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


def choose_discount() -> DiscountStrategy:
    print("Discount: 1. None   2. Percentage   3. Bulk   4. Student (5% off)")
    choice = input("Choose discount (1-4, Enter for none): ").strip()
    try:
        if choice == "2":
            return PercentageDiscount(get_non_negative_float("Percent off (0-100): "))
        if choice == "3":
            threshold = get_non_negative_float("Order total needed: ")
            amount = get_non_negative_float("Amount off: ")
            return BulkDiscount(threshold, amount)
        if choice == "4":
            return StudentDiscount()
    except ValueError as error:
        print(f"{error} No discount applied.")
    return NoDiscount()


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
            order.add_order_line(product, quantity)  # the Order validates the quantity
            print("Added to order.")
        except ValueError:
            print("Quantity must be a whole number greater than zero.")

    if not order.get_order_lines():
        print("Order cancelled - no items were added.")
        return
    order.set_discount(choose_discount())
    print()
    order.display_information()


def import_products_action(inventory: Inventory, suppliers: list[Supplier]) -> None:
    supplier = choose_supplier(suppliers)
    if supplier is None:
        return
    path = input("CSV file (Enter for products.csv): ").strip() or "products.csv"
    load_products(path, inventory, supplier)


def print_menu() -> None:
    print("\n=== Inventory Management System ===")
    print("1. Display all products")
    print("2. Add a product")
    print("3. Update stock")
    print("4. Search for a product")
    print("5. Remove a product")
    print("6. Create an order")
    print("7. Import products from CSV")
    print("8. Save inventory")
    print("9. Exit")


def load_sample_data(inventory: Inventory, suppliers: list[Supplier]) -> None:
    techsource = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.com")
    softworks = Supplier("S002", "SoftWorks Studio", "hello@softworks.com")
    suppliers.append(techsource)
    suppliers.append(softworks)
    inventory.add_product(ProductFactory.create(
        "physical", "L001", "Laptop", 1200.00, 15, techsource, 2.5))
    inventory.add_product(ProductFactory.create(
        "digital", "L003", "Photo Suite", 49.99, 100, softworks, 450.0))


def main() -> None:
    inventory = Inventory()
    suppliers: list[Supplier] = []

    if not load_inventory(inventory, suppliers):
        inventory = Inventory()
        suppliers = []
        load_sample_data(inventory, suppliers)

    while True:
        print_menu()
        choice = input("Choose an option (1-9): ").strip()

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
            import_products_action(inventory, suppliers)
        elif choice == "8":
            save_inventory(inventory, suppliers)
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please enter a number from 1 to 9.")


if __name__ == "__main__":
    main()
