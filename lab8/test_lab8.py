"""Lab 8 checks. Run with:  python test_lab8.py"""
import inspect
import os

import main
from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory
from order_line import OrderLine
from order import Order

passed: int = 0
failed: int = 0


def check(description: str, condition: bool) -> None:
    global passed, failed
    if condition:
        passed += 1
        print(f"  [PASS] {description}")
    else:
        failed += 1
        print(f"  [FAIL] {description}")


def show_product_details(product: Product) -> None:
    """LSP test: works for ANY Product, without knowing its subclass."""
    product.display_information()
    print(f"    -> {product.get_fulfilment_info()}")


def fully_type_hinted(cls: type) -> bool:
    """True if every method parameter and return value has a type hint."""
    for _, method in inspect.getmembers(cls, inspect.isfunction):
        signature = inspect.signature(method)
        if signature.return_annotation is inspect.Signature.empty:
            return False
        for parameter in signature.parameters.values():
            if parameter.name != "self" and parameter.annotation is inspect.Parameter.empty:
                return False
    return True


# =====================================================================
print("\n=== 2. ASSOCIATION: Supplier and Product ===")
supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.com")
laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.5)
editor = DigitalProduct("D001", "Photo Editor", 49.99, 100, supplier, 450.0)

print("Supplier information through each product:")
laptop.get_supplier().display_information()
editor.get_supplier().display_information()
check("laptop stores a reference to its Supplier", laptop.get_supplier() is supplier)
check("editor stores a reference to its Supplier", editor.get_supplier() is supplier)
check("Supplier is a separate object from the products",
      supplier is not laptop and supplier is not editor)

print("\nPREDICT FIRST #1: what happens if we `del supplier` after creating the products?")
del supplier
try:
    print(supplier)  # type: ignore[name-defined]
except NameError:
    print("  The variable name 'supplier' is gone.")
print("  Can the products still show their supplier?")
laptop.get_supplier().display_information()
editor.get_supplier().display_information()
check("products still reach their Supplier after `del supplier`",
      laptop.get_supplier().get_name() == "TechSource Pte Ltd")

# =====================================================================
print("\n=== 3. AGGREGATION: Inventory and Product ===")
softworks = Supplier("S002", "SoftWorks Studio", "hello@softworks.com")
guitar = PhysicalProduct("P003", "Guitar", 350.00, 5, softworks, 3.5)  # made BEFORE any inventory
inventory_a = Inventory()
inventory_b = Inventory()
check("product exists before it is in any inventory", guitar.get_name() == "Guitar")

check("add guitar to Inventory A", inventory_a.add_product(guitar))
check("find_product returns the SAME object", inventory_a.find_product("P003") is guitar)
check("find_product returns None when missing", inventory_a.find_product("NOPE") is None)

print("\nPREDICT FIRST #2: will the guitar still work after it is removed from Inventory A?")
check("remove guitar from Inventory A", inventory_a.remove_product("P003"))
check("Inventory A no longer holds it", inventory_a.find_product("P003") is None)
guitar.display_information()
guitar.update_stock(7)
check("guitar still works after removal (stock now 7)", guitar.get_stock() == 7)

check("add the SAME guitar object to Inventory B", inventory_b.add_product(guitar))
check("Inventory B holds the very same object", inventory_b.find_product("P003") is guitar)

inventory_b.remove_product("P003")
check("emptied Inventory B has no products", len(inventory_b.get_products()) == 0)
check("the Product itself was NOT destroyed", guitar.get_name() == "Guitar")

# =====================================================================
print("\n=== 4. COMPOSITION: Order and OrderLine ===")
order_1 = Order("O001")
order_1.add_order_line(laptop, 1)
order_1.add_order_line(editor, 2)
order_1.display_information()
check("order total = 1200.00 + 2 x 49.99",
      abs(order_1.calculate_total() - 1299.98) < 0.001)
check("Order created its own OrderLines", len(order_1.get_order_lines()) == 2)
check("OrderLine refers to the Product (does not copy it)",
      order_1.get_order_lines()[0].get_product() is laptop)

print("\nPREDICT FIRST #3: same Product in two Orders - how many OrderLines? how many Products?")
order_2 = Order("O002")
order_2.add_order_line(laptop, 3)
line_1: OrderLine = order_1.get_order_lines()[0]
line_2: OrderLine = order_2.get_order_lines()[0]
print(f"  OrderLine in order 1: id = {id(line_1)}")
print(f"  OrderLine in order 2: id = {id(line_2)}")
print(f"  Product via line 1:   id = {id(line_1.get_product())}")
print(f"  Product via line 2:   id = {id(line_2.get_product())}")
check("two DIFFERENT OrderLine objects", line_1 is not line_2)
check("ONE shared Product object", line_1.get_product() is line_2.get_product())

check("remove an order line through the Order", order_1.remove_order_line("D001"))
check("order total updated to 1200.00", abs(order_1.calculate_total() - 1200.00) < 0.001)
try:
    OrderLine(laptop, 0)
    check("OrderLine rejects quantity 0", False)
except ValueError:
    check("OrderLine rejects quantity 0", True)

del order_2
check("deleting an Order does NOT destroy the Product", laptop.get_name() == "Laptop")

# =====================================================================
print("\n=== 5. TYPE HINTS ===")
print("  Inventory.find_product hints:", Inventory.find_product.__annotations__)
print("  Order.add_order_line hints:  ", Order.add_order_line.__annotations__)
for cls in (Supplier, Product, PhysicalProduct, DigitalProduct, CanBeShipped,
            Inventory, OrderLine, Order):
    check(f"{cls.__name__}: every method parameter and return is type-hinted",
          fully_type_hinted(cls))

# =====================================================================
print("\n=== 6. LISKOV SUBSTITUTION PRINCIPLE ===")
print("show_product_details() called with a PhysicalProduct and a DigitalProduct:")
show_product_details(laptop)
show_product_details(editor)

for product in (laptop, editor):
    product.update_stock(20)
    check(f"{product.get_name()}: update_stock(20) keeps its meaning",
          product.get_stock() == 20)
    try:
        product.update_stock(-1)
        check(f"{product.get_name()}: negative stock rejected", False)
    except ValueError:
        check(f"{product.get_name()}: negative stock rejected", True)
check("neither subclass overrides update_stock (same promise as Product)",
      PhysicalProduct.update_stock is Product.update_stock
      and DigitalProduct.update_stock is Product.update_stock)
laptop.update_stock(15)   # put the stock back to the starting values
editor.update_stock(100)

print("\nDemo of a BAD subclass (the teammate's idea from the lab):")


class BrokenDigitalProduct(DigitalProduct):
    def update_stock(self, quantity: int) -> None:
        raise NotImplementedError("Digital products have no stock")


def restock_everything(products: list[Product]) -> None:
    """Normal Product code: it just trusts that update_stock() works."""
    for product in products:
        product.update_stock(50)


try:
    broken = BrokenDigitalProduct("D999", "Broken", 1.00, 1, softworks, 1.0)
    restock_everything([guitar, broken])
    check("broken subclass works with Product code", True)
except NotImplementedError as error:
    print(f"  Crashed with NotImplementedError: {error}")
    check("LSP violation shown: the broken subclass cannot stand in for Product", True)

# =====================================================================
print("\n=== 7. POLYMORPHISM through the Product type ===")
inventory = Inventory()
inventory.add_product(laptop)
inventory.add_product(editor)
inventory.add_product(PhysicalProduct("P002", "Mouse", 25.50, 40, softworks, 0.2))

print("PREDICT FIRST #4: what will get_fulfilment_info() print for each product?")
for product in inventory.get_products():  # one loop, no isinstance()
    print(f"  {product.get_name():<13} -> {product.get_fulfilment_info()}")
print("\nAnd display_all():")
inventory.display_all()
check("physical products give shipping info",
      "shipping" in inventory.find_product("P001").get_fulfilment_info().lower())
check("digital products give download info",
      "digital" in inventory.find_product("D001").get_fulfilment_info().lower())

# =====================================================================
print("\n=== 9. OTHER CHECKS ===")
try:
    Product("X", "X", 1.0, 1, softworks)  # type: ignore[abstract]
    check("Product() is blocked", False)
except TypeError:
    check("Product() is blocked (abstract)", True)
check("physical product can be shipped", isinstance(laptop, CanBeShipped))
check("digital product is not CanBeShipped", not isinstance(editor, CanBeShipped))

print("\nJSON persistence with suppliers and both product types:")
main.FILENAME = "test_inventory.json"
test_suppliers: list[Supplier] = [laptop.get_supplier(), softworks]
main.save_inventory(inventory, test_suppliers)
reloaded = Inventory()
reloaded_suppliers: list[Supplier] = []
main.load_inventory(reloaded, reloaded_suppliers)
check("same number of products after reload", len(reloaded.get_products()) == 3)
check("laptop reloaded as PhysicalProduct",
      isinstance(reloaded.find_product("P001"), PhysicalProduct))
check("editor reloaded as DigitalProduct",
      isinstance(reloaded.find_product("D001"), DigitalProduct))
check("reloaded products share ONE Supplier object",
      reloaded.find_product("P001").get_supplier() is reloaded.find_product("D001").get_supplier())
os.remove("test_inventory.json")

print(f"\nResults: {passed} passed, {failed} failed")
