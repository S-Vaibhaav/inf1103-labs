from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """STRATEGY pattern: every discount offers the same apply() method.
    The Order only calls apply(); it never knows which discount it has."""

    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    """PercentageDiscount(10) takes 10% off."""

    def __init__(self, percent: float) -> None:
        if percent < 0 or percent > 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.__percent: float = percent

    def apply(self, total: float) -> float:
        return total * (1 - self.__percent / 100)


class BulkDiscount(DiscountStrategy):
    """BulkDiscount(200, 20) takes 20 off any total of 200 or more."""

    def __init__(self, threshold: float, amount: float) -> None:
        if threshold < 0 or amount < 0:
            raise ValueError("Threshold and amount cannot be negative.")
        self.__threshold: float = threshold
        self.__amount: float = amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return max(total - self.__amount, 0.0)
        return total


class StudentDiscount(DiscountStrategy):
    """Our fourth strategy: 5% off. Added WITHOUT changing Order."""

    def apply(self, total: float) -> float:
        return total * 0.95
