"""Prints the real result of every 'Predict first' question. Run: python demo_predict_first.py"""
import contextlib
import io
import re
import subprocess
import sys
import traceback
from pathlib import Path
from unittest import mock

from supplier import Supplier
from inventory import Inventory
from order import Order
from discount_strategy import BulkDiscount, PercentageDiscount
from product_factory import ProductFactory
from product_loader import load_products
from input_helpers import get_positive_float

supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.com")
desk = ProductFactory.create("physical", "P1", "Desk", 125.0, 10, supplier, 5.0)


def heading(text: str) -> None:
    print(f"\n=== {text} ===")


heading("2.3  Order lines add up to 250")
order = Order("O1", BulkDiscount(200, 20))
order.add_order_line(desk, 2)
print(f"BulkDiscount(200, 20)               -> {order.calculate_total():.2f}")
order.set_discount(PercentageDiscount(10))
print(f"then set_discount(PercentageDiscount(10)) -> {order.calculate_total():.2f}")

heading("2.4  Can two orders share one PercentageDiscount object?")
shared = PercentageDiscount(10)
order_a, order_b = Order("A", shared), Order("B", shared)
order_a.add_order_line(desk, 1)
order_b.add_order_line(desk, 2)
print(f"Order A total {order_a.calculate_total():.2f}, Order B total {order_b.calculate_total():.2f}")
print("They use the very same strategy object (shared)")

heading("3.2  ProductFactory.create('service', ...)")
try:
    ProductFactory.create("service", "S1", "Install", 30.0, 5, supplier)
except ValueError as error:
    last = traceback.extract_tb(error.__traceback__)[-1]
    print(f"ValueError: {error}")
    print(f"Raised on line {last.lineno} of {last.filename.split('/')[-1]}:  {last.line}")
result = subprocess.run(
    [sys.executable, "-c",
     "from supplier import Supplier\nfrom product_factory import ProductFactory\n"
     "ProductFactory.create('service', 'S1', 'Install', 30.0, 5, Supplier('S','n','e'))"],
    capture_output=True, text=True)
print("If nothing catches it, the program stops with a traceback. Last line:")
print("  " + result.stderr.strip().splitlines()[-1])

heading("3.3  Where are products created directly now?")
for path in sorted(Path(".").glob("*.py")):
    if path.name.startswith("demo_"):
        continue
    count = sum(1 for line in path.read_text().splitlines()
                if re.search(r"\b(PhysicalProduct|DigitalProduct)\(", line)
                and not line.strip().startswith("class "))
    if count:
        print(f"  {path.name}: {count} direct constructor call(s)")
print("  (every other file asks ProductFactory.create instead)")

heading("4  Should DigitalProduct be allowed to skip the stock rule?")
for kind in ("physical", "digital"):
    product = ProductFactory.create(kind, "X", "Item", 10.0, 5, supplier, 1.0)
    try:
        product.update_stock(-1)
    except ValueError as error:
        print(f"  {kind}: update_stock(-1) -> ValueError: {error}")

heading("5.1  User types: abc, -5, 12.50")
with mock.patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
    value = get_positive_float("Price: ")
print(f"Returned: {value}")

heading("5.2  Loading products.csv")
inventory = Inventory()
load_products("products.csv", inventory, supplier)
heading("5.2  Loading a file that does not exist (products.csv renamed)")
load_products("products_renamed.csv", inventory, supplier)
