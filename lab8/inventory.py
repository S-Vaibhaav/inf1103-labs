from product import Product


class Inventory:
    """Manages a COLLECTION of Product objects.

    AGGREGATION: the Inventory holds references to products but does not
    create them or own their lifecycle. Removing a product from the
    inventory only removes the reference - the Product object lives on.

    It is typed with the base class Product, so it can hold ANY product type.
    """

    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        """Add an existing Product. Returns False if the ID already exists."""
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> bool:
        """Remove the reference to a product. Returns False if not found."""
        product = self.find_product(product_id)
        if product is None:
            return False
        self.__products.remove(product)  # only the reference is removed
        return True

    def find_product(self, product_id: str) -> Product | None:
        """Find ONE product by exact ID. Returns the Product, or None."""
        for product in self.__products:
            if product.get_product_id().lower() == product_id.lower():
                return product
        return None

    def search_product(self, keyword: str) -> list[Product]:
        """Find all products whose ID or name contains the keyword."""
        keyword = keyword.lower()
        results: list[Product] = []
        for product in self.__products:
            if (keyword in product.get_product_id().lower()
                    or keyword in product.get_name().lower()):
                results.append(product)
        return results

    def display_all(self) -> None:
        if not self.__products:
            print("The inventory is empty.")
            return
        for product in self.__products:
            product.display_information()  # polymorphism: no isinstance needed

    def get_products(self) -> list[Product]:
        """Give back a COPY of the list so outside code can't change ours."""
        return list(self.__products)
