from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    """Abstract base class for every product. Cannot be created directly.

    VALIDATION lives here, in the class that owns the rules:
    price must be greater than zero, stock can never be negative.
    """

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier) -> None:
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = 0
        self.update_stock(stock)  # the stock rule lives in ONE place
        self.__supplier: Supplier = supplier

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self, quantity: int) -> None:
        """Set the stock to a new value. Negative stock is never allowed."""
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = quantity

    def display_information(self) -> None:
        print(
            f"ID: {self.__product_id:<6} | "
            f"Name: {self.__name:<15} | "
            f"Price: ${self.__price:>8.2f} | "
            f"Stock: {self.__stock}"
        )
        print(f"    Supplier: {self.__supplier.get_name()}")

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Explain how this product gets to the customer."""
        pass
