import ast
import inspect
import unittest

from discount_strategy import (DiscountStrategy, NoDiscount, PercentageDiscount,
                               BulkDiscount, StudentDiscount)
from order import Order
from product_factory import ProductFactory
from supplier import Supplier


class StrategyTests(unittest.TestCase):
    def setUp(self) -> None:
        supplier = Supplier("S1", "Acme", "a@acme.com")
        self.product = ProductFactory.create("physical", "P1", "Desk", 125.0, 10, supplier, 5.0)

    def make_order(self, quantity: int = 2, discount: DiscountStrategy | None = None) -> Order:
        order = Order("O1", discount)
        order.add_order_line(self.product, quantity)  # 125 x 2 = 250
        return order

    def test_default_is_no_discount(self) -> None:
        self.assertEqual(self.make_order().calculate_total(), 250.0)

    def test_bulk_discount_on_250(self) -> None:
        self.assertEqual(self.make_order(2, BulkDiscount(200, 20)).calculate_total(), 230.0)

    def test_bulk_discount_below_threshold(self) -> None:
        self.assertEqual(self.make_order(1, BulkDiscount(200, 20)).calculate_total(), 125.0)

    def test_percentage_and_student(self) -> None:
        self.assertEqual(self.make_order(2, PercentageDiscount(10)).calculate_total(), 225.0)
        self.assertEqual(self.make_order(2, StudentDiscount()).calculate_total(), 237.5)

    def test_set_discount_changes_existing_order(self) -> None:
        order = self.make_order(2, BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230.0)
        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225.0)

    def test_new_strategy_needs_no_change_to_order(self) -> None:
        class HalfPrice(DiscountStrategy):  # brand new strategy, defined here in the test
            def apply(self, total: float) -> float:
                return total / 2

        self.assertEqual(self.make_order(2, HalfPrice()).calculate_total(), 125.0)

    def test_two_orders_can_share_one_strategy(self) -> None:
        shared = PercentageDiscount(10)
        self.assertEqual(self.make_order(1, shared).calculate_total(), 112.5)
        self.assertEqual(self.make_order(2, shared).calculate_total(), 225.0)

    def test_order_has_no_discount_branching(self) -> None:
        tree = ast.parse(inspect.getsource(Order))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name in (
                    "__init__", "set_discount", "calculate_total"):
                for inner in ast.walk(node):
                    self.assertNotIsInstance(inner, (ast.If, ast.IfExp),
                                             f"if/elif found in Order.{node.name}")
                code = ast.unparse(node).lower()
                self.assertNotIn("percentage", code.replace("percentagediscount", ""))
                self.assertNotIn("bulk", code)

    def test_invalid_strategy_values_rejected(self) -> None:
        with self.assertRaises(ValueError):
            PercentageDiscount(150)
        with self.assertRaises(ValueError):
            BulkDiscount(-1, 5)

    def test_discount_strategy_is_abstract(self) -> None:
        with self.assertRaises(TypeError):
            DiscountStrategy()  # type: ignore[abstract]
        self.assertEqual(NoDiscount().apply(99.0), 99.0)


if __name__ == "__main__":
    unittest.main()
