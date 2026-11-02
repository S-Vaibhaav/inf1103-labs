"""Lab 7 checks. Run with:  python test_lab7.py"""
import os

import main
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory

passed = 0
failed = 0


def check(description, condition):
    global passed, failed
    if condition:
        passed += 1
        print(f"  [PASS] {description}")
    else:
        failed += 1
        print(f"  [FAIL] {description}")


print("\n1. Physical product stores and displays its weight")
laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.5)
laptop.display_information()
check("weight is stored", laptop.get_weight() == 2.5)

print("\n2. Digital product stores and displays its download size")
editor = DigitalProduct("D001", "Photo Editor", 49.99, 100, 450.0)
editor.display_information()
check("download size is stored", editor.get_download_size() == 450.0)

print("\n3. Both subclasses implement get_fulfilment_info()")
print("  Physical:", laptop.get_fulfilment_info())
print("  Digital: ", editor.get_fulfilment_info())
check("physical mentions shipping", "shipping" in laptop.get_fulfilment_info().lower())
check("digital mentions digital", "digital" in editor.get_fulfilment_info().lower())

print("\n4. The abstract Product class cannot be created directly")
try:
    Product("X001", "Mystery", 1.00, 1)
    check("Product() was blocked", False)
except TypeError as error:
    print("  TypeError:", error)
    check("Product() was blocked", True)

print("\n5. Physical products calculate shipping costs")
for weight, expected in [(0.5, 6.00), (2.0, 9.00), (10.0, 25.00)]:
    item = PhysicalProduct("T", "Test", 1.00, 1, weight)
    cost = item.calculate_shipping_cost()
    print(f"  {weight:>4} kg -> ${cost:.2f}")
    check(f"{weight} kg costs ${expected:.2f}", abs(cost - expected) < 0.001)

print("\n6. Digital products are not required to ship")
check("physical IS a CanBeShipped", isinstance(laptop, CanBeShipped))
check("digital is NOT a CanBeShipped", not isinstance(editor, CanBeShipped))
check("digital has no shipping method", not hasattr(editor, "calculate_shipping_cost"))
try:
    CanBeShipped()
    check("CanBeShipped() was blocked", False)
except TypeError:
    check("CanBeShipped() was blocked (interface can't be created)", True)

print("\n7. Inventory operations still work")
inventory = Inventory()
check("add physical product", inventory.add_product(laptop))
check("add digital product", inventory.add_product(editor))
check("duplicate ID is rejected", not inventory.add_product(laptop))
check("search 'lap' finds the laptop", len(inventory.search_product("lap")) == 1)
inventory.get_product("P001").update_stock(30)
check("update stock to 30", inventory.get_product("P001").get_stock() == 30)
try:
    inventory.get_product("P001").update_stock(-5)
    check("negative stock rejected", False)
except ValueError:
    check("negative stock rejected", True)
print("  display_all():")
inventory.display_all()

print("\n8. JSON saving and loading keep the correct types")
main.FILENAME = "test_inventory.json"  # use a temporary file for this test
main.save_inventory(inventory)
reloaded = Inventory()
main.load_inventory(reloaded)
check("same number of products", len(reloaded.get_products()) == 2)
check("laptop reloaded as PhysicalProduct",
      isinstance(reloaded.get_product("P001"), PhysicalProduct))
check("laptop weight kept", reloaded.get_product("P001").get_weight() == 2.5)
check("laptop updated stock kept", reloaded.get_product("P001").get_stock() == 30)
check("editor reloaded as DigitalProduct",
      isinstance(reloaded.get_product("D001"), DigitalProduct))
check("editor download size kept", reloaded.get_product("D001").get_download_size() == 450.0)
os.remove("test_inventory.json")

print(f"\nResults: {passed} passed, {failed} failed")
