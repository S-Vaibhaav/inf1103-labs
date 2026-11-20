import ast
import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from input_helpers import get_positive_float
from inventory import Inventory
from product_loader import load_products
from supplier import Supplier

CSV_TEXT = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""


def run_loader(path: str, inventory: Inventory) -> list[str]:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        load_products(path, inventory, Supplier("S1", "Acme", "a@acme.com"))
    return buffer.getvalue().strip().splitlines()


class InputTests(unittest.TestCase):
    def test_keeps_asking_until_valid(self) -> None:
        buffer = io.StringIO()
        with mock.patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            with contextlib.redirect_stdout(buffer):
                value = get_positive_float("Price: ")
        self.assertEqual(value, 12.5)
        self.assertEqual(buffer.getvalue().strip().splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])

    def test_zero_is_rejected(self) -> None:
        with mock.patch("builtins.input", side_effect=["0", "3"]):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(get_positive_float("Price: "), 3.0)


class LoadingTests(unittest.TestCase):
    def test_bad_rows_skipped_and_good_rows_load(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "products.csv"
            path.write_text(CSV_TEXT)
            inventory = Inventory()
            lines = run_loader(str(path), inventory)
        self.assertEqual([p.get_product_id() for p in inventory.get_products()],
                         ["P001", "D001", "P003"])
        self.assertEqual(lines, [
            "Skipping line 4: Unknown product type: service",
            "Skipping line 5: price must be a number and stock must be a whole number.",
            "3 products loaded.",
            "Load attempt finished.",
        ])

    def test_missing_file_is_handled(self) -> None:
        inventory = Inventory()
        lines = run_loader("does_not_exist.csv", inventory)
        self.assertEqual(lines, ["Products file not found: does_not_exist.csv",
                                 "Load attempt finished."])
        self.assertEqual(inventory.get_products(), [])

    def test_duplicate_id_is_reported_not_crashed(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "dup.csv"
            path.write_text("h\nphysical,P1,Lamp,5.0,1\nphysical,P1,Lamp,5.0,1\n")
            inventory = Inventory()
            lines = run_loader(str(path), inventory)
        self.assertEqual(len(inventory.get_products()), 1)
        self.assertIn("1 products loaded.", lines)


class ExceptionStyleTests(unittest.TestCase):
    def test_every_except_names_a_specific_exception(self) -> None:
        root = Path(__file__).parent.parent
        for path in root.glob("*.py"):
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, ast.ExceptHandler):
                    self.assertIsNotNone(node.type, f"bare except in {path.name}")
                    names = ast.dump(node.type)
                    self.assertNotIn("'Exception'", names, f"except Exception in {path.name}")


if __name__ == "__main__":
    unittest.main()
