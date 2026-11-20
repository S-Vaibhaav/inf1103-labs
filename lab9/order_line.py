from product import Product


class OrderLine:
    """One product + quantity inside ONE order.

    COMPOSITION: an OrderLine is created only by an Order and belongs to it.
    It REFERS to a Product (association) but does not own it.
    """

    def __init__(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be at least 1.")
        self.__product: Product = product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None:
        print(
            f"    {self.__product.get_name():<15} "
            f"x {self.__quantity:<3} "
            f"@ ${self.__product.get_price():>8.2f} "
            f"= ${self.calculate_subtotal():>9.2f}"
        )
