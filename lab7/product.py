from abc import ABC, abstractmethod


class Product(ABC):
    """Abstract base class for every product.

    Because it has an abstract method, you can NOT create a Product directly.
    You must create a PhysicalProduct or a DigitalProduct instead.
    """

    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    # ---- Getters ----
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    # ---- Normal (concrete) methods: children inherit these ----
    def update_stock(self, quantity):
        """Set the stock to a new value. The Product decides what is allowed."""
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = quantity

    def display_information(self):
        """Prints the information that EVERY product has."""
        print(
            f"ID: {self.__product_id:<6} | "
            f"Name: {self.__name:<15} | "
            f"Price: ${self.__price:>8.2f} | "
            f"Stock: {self.__stock}"
        )

    # ---- Abstract method: NO code here, every child MUST write its own ----
    @abstractmethod
    def get_fulfilment_info(self):
        """Explain how this product gets to the customer."""
        pass
