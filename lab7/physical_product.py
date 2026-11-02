from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    """A physical product IS-A Product (inheritance) and CAN BE shipped
    (it signs the CanBeShipped contract)."""

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)  # reuse Product's constructor
        self.__weight = weight  # in kilograms

    def get_weight(self):
        return self.__weight

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def calculate_shipping_cost(self):
        # Simple rule: $5.00 base fee + $2.00 for every kg
        return 5.00 + 2.00 * self.__weight

    def display_information(self):
        super().display_information()  # parent prints the common info
        print(f"    Weight: {self.__weight:.2f} kg | "
              f"Shipping cost: ${self.calculate_shipping_cost():.2f}")
        print(f"    Fulfilment: {self.get_fulfilment_info()}")
