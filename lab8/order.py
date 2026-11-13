from order_line import OrderLine
from product import Product


class Order:
    """A customer order.

    COMPOSITION: the Order CREATES and manages its own OrderLine objects.
    Nobody else creates an OrderLine and hands it in, and a line never
    moves to another Order. If the Order goes, its lines go with it.
    """

    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

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
        total: float = 0.0
        for order_line in self.__order_lines:
            total += order_line.calculate_subtotal()
        return total

    def display_information(self) -> None:
        print(f"Order {self.__order_id}")
        if not self.__order_lines:
            print("    (no items)")
        for order_line in self.__order_lines:
            order_line.display_information()
        print(f"    Order total: ${self.calculate_total():.2f}")
