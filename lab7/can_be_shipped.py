from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface-style contract: 'anything that can be shipped must be able
    to calculate its shipping cost'. No attributes and no code inside."""

    @abstractmethod
    def calculate_shipping_cost(self):
        pass
