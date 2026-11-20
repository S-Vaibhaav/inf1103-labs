import unittest
from pathlib import Path

from digital_product import DigitalProduct
from order_line import OrderLine
from physical_product import PhysicalProduct
from product import Product
from product_factory import ProductFactory
from supplier import Supplier


class FactoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S1", "Acme", "a@acme.com")

    def test_creates_correct_types(self) -> None:
        physical = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10, self.supplier, 1.5)
        digital = ProductFactory.create("digital", "D1", "Editor", 49.9, 100, self.supplier, 300.0)
        self.assertIsInstance(physical, PhysicalProduct)
        self.assertIsInstance(digital, DigitalProduct)
        self.assertIsInstance(physical, Product)
        self.assertEqual(physical.get_weight(), 1.5)

    def test_unknown_type_raises_clear_error(self) -> None:
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S1", "Install", 30.0, 5, self.supplier)
        self.assertIn("Unknown product type: service", str(context.exception))

    def test_main_does_not_create_products_directly(self) -> None:
        text = (Path(__file__).parent.parent / "main.py").read_text()
        self.assertNotIn("PhysicalProduct(", text)
        self.assertNotIn("DigitalProduct(", text)

    def test_product_is_still_abstract(self) -> None:
        with self.assertRaises(TypeError):
            Product("X", "X", 1.0, 1, self.supplier)  # type: ignore[abstract]


class ValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S1", "Acme", "a@acme.com")

    def test_price_must_be_greater_than_zero(self) -> None:
        for bad_price in (0, -5.0):
            with self.assertRaises(ValueError):
                ProductFactory.create("physical", "P1", "Lamp", bad_price, 1, self.supplier)

    def test_stock_cannot_be_negative(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D1", "Editor", 10.0, -1, self.supplier)
        product = ProductFactory.create("physical", "P1", "Lamp", 10.0, 3, self.supplier)
        with self.assertRaises(ValueError):
            product.update_stock(-1)

    def test_digital_product_keeps_the_same_stock_rule(self) -> None:  # LSP
        self.assertIs(DigitalProduct.update_stock, Product.update_stock)
        self.assertIs(PhysicalProduct.update_stock, Product.update_stock)

    def test_order_line_quantity_must_be_greater_than_zero(self) -> None:
        product = ProductFactory.create("physical", "P1", "Lamp", 10.0, 3, self.supplier)
        for bad_quantity in (0, -2):
            with self.assertRaises(ValueError):
                OrderLine(product, bad_quantity)
        self.assertEqual(OrderLine(product, 2).calculate_subtotal(), 20.0)


if __name__ == "__main__":
    unittest.main()
