from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    """A physical product IS-A Product and CAN BE shipped."""

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float) -> None:
        # Pass everything the parent needs (including the Supplier) up with super()
        super().__init__(product_id, name, price, stock, supplier)
        if weight < 0:
            raise ValueError("Weight cannot be negative.")
        self.__weight: float = weight  # in kilograms

    def get_weight(self) -> float:
        return self.__weight

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        # Simple rule: $5.00 base fee + $2.00 for every kg
        return 5.00 + 2.00 * self.__weight

    def display_information(self) -> None:
        super().display_information()  # parent prints the common info
        print(f"    Weight: {self.__weight:.2f} kg | "
              f"Shipping cost: ${self.calculate_shipping_cost():.2f}")
        print(f"    Fulfilment: {self.get_fulfilment_info()}")
