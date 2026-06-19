from dataclasses import dataclass

from src.constants import COIN_DENOMINATIONS


@dataclass
class Coins:
    denomination: str
    quantity: int

    def __post_init__(self) -> None:
        if self.denomination not in COIN_DENOMINATIONS:
            raise ValueError(
                f"Invalid denomination: '{self.denomination}'. "
                f"Must be one of: {list(COIN_DENOMINATIONS.keys())}"
            )
        if self.quantity < 0:
            raise ValueError(f"Quantity must be non-negative, got {self.quantity}.")

