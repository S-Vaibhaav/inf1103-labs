from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


class ProductFactory:
    """FACTORY pattern: the one place that decides which Product to build.
    It returns the base type Product, so callers never name a subclass."""

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock: int, supplier: Supplier, extra: float = 0.0) -> Product:
        """extra = weight in kg (physical) or download size in MB (digital)."""
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock, supplier, extra)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock, supplier, extra)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
