from discount_strategy import DiscountStrategy, NoDiscount
from order_line import OrderLine
from product import Product


class Order:
    """A customer order.

    COMPOSITION with OrderLine (the Order creates its own lines).
    ASSOCIATION with DiscountStrategy (the Order USES a strategy that can be
    shared with other orders). There is no if/elif about discount types here.
    """

    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = discount or NoDiscount()  # default: none

    def get_order_id(self) -> str:
        return self.__order_id

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.__discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)  # the Order creates it
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        """Remove the line for a product. Returns False if not found."""
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id().lower() == product_id.lower():
                self.__order_lines.remove(order_line)
                return True
        return False

    def get_order_lines(self) -> list[OrderLine]:
        return list(self.__order_lines)

    def calculate_total(self) -> float:
        total = sum((line.calculate_subtotal() for line in self.__order_lines), 0.0)
        return self.__discount.apply(total)

    def display_information(self) -> None:
        print(f"Order {self.__order_id}")
        if not self.__order_lines:
            print("    (no items)")
        for order_line in self.__order_lines:
            order_line.display_information()
        print(f"    Order total: ${self.calculate_total():.2f}")
