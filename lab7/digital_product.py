from product import Product


class DigitalProduct(Product):
    """A digital product IS-A Product. It is NOT shipped, so it does not
    use the CanBeShipped interface."""

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)  # reuse Product's constructor
        self.__download_size = download_size  # in megabytes

    def get_download_size(self):
        return self.__download_size

    def get_fulfilment_info(self):
        return "This product is delivered digitally (download link)."

    def display_information(self):
        super().display_information()  # parent prints the common info
        print(f"    Download size: {self.__download_size:.1f} MB")
        print(f"    Fulfilment: {self.get_fulfilment_info()}")
