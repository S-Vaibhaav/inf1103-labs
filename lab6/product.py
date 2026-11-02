class Product:
    """Represents and manages ONE product (Single Responsibility)."""

    def __init__(self, product_id, name, price, stock):
        # Double underscore = "treat this as private" (Python name mangling)
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    # ---- Getters: let other code READ the data without touching it directly ----
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    # ---- Methods from the class diagram ----
    def update_stock(self, quantity):
        """Set the stock to a new value. The Product decides what is allowed."""
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = quantity

    def display_information(self):
        print(
            f"ID: {self.__product_id:<6} | "
            f"Name: {self.__name:<15} | "
            f"Price: ${self.__price:>8.2f} | "
            f"Stock: {self.__stock}"
        )
