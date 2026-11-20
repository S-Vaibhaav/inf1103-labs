import csv

from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Load products from a CSV file. Bad rows are reported and skipped."""
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row
            for line_number, row in enumerate(reader, start=2):
                if not row:
                    continue
                if len(row) != 5:
                    print(f"Skipping line {line_number}: expected 5 columns.")
                    continue
                product_type, product_id, name, price_text, stock_text = row
                try:
                    price = float(price_text)
                    stock = int(stock_text)
                except ValueError:
                    print(f"Skipping line {line_number}: price must be a number "
                          f"and stock must be a whole number.")
                    continue
                try:
                    product = ProductFactory.create(
                        product_type.strip(), product_id.strip(), name.strip(),
                        price, stock, supplier)
                except ValueError as error:
                    print(f"Skipping line {line_number}: {error}")
                    continue
                if inventory.add_product(product):
                    loaded += 1
                else:
                    print(f"Skipping line {line_number}: product ID "
                          f"{product_id} already exists.")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
