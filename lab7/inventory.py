class Inventory:
    """Manages a COLLECTION of Product objects (Single Responsibility)."""

    def __init__(self):
        self.__products = []  # a list that will hold Product objects

    def add_product(self, product):
        """Add a product. Returns False if the ID already exists."""
        if self.get_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def get_product(self, product_id):
        """Find ONE product by exact ID. Returns the Product, or None."""
        for product in self.__products:
            if product.get_product_id().lower() == product_id.lower():
                return product
        return None

    def search_product(self, keyword):
        """Find all products whose ID or name contains the keyword."""
        keyword = keyword.lower()
        results = []
        for product in self.__products:
            if (keyword in product.get_product_id().lower()
                    or keyword in product.get_name().lower()):
                results.append(product)
        return results

    def display_all(self):
        if not self.__products:
            print("The inventory is empty.")
            return
        for product in self.__products:
            product.display_information()

    def get_products(self):
        """Give back a COPY of the list so outside code can't change ours."""
        return list(self.__products)
