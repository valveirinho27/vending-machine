from dataclasses import dataclass


@dataclass
class Product:
    name: str
    amount: int
    price: int  # price in pence

    def __post_init__(self) -> None:
        if self.price <= 0:
            raise ValueError(f"Price must be positive, got {self.price}.")
        if self.amount < 0:
            raise ValueError(f"Amount must be non-negative, got {self.amount}.")

