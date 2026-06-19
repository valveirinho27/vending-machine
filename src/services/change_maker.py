from dataclasses import dataclass

from src.constants import COIN_DENOMINATIONS


@dataclass(frozen=True)
class ChangePlan:
    coins: list[str]
    remaining: int

    @property
    def exact(self) -> bool:
        return self.remaining == 0


class ChangeMaker:
    """Service responsible for calculating change from an inventory."""

    @staticmethod
    def calculate(amount: int, inventory: dict[str, int]) -> ChangePlan:
        if amount < 0:
            raise ValueError(f"Amount must be non-negative, got {amount}.")

        change_to_return: list[str] = []
        remaining = amount

        for denomination in sorted(COIN_DENOMINATIONS, key=lambda d: COIN_DENOMINATIONS[d], reverse=True):
            value = COIN_DENOMINATIONS[denomination]
            available = inventory.get(denomination, 0)
            while remaining >= value and available > 0:
                change_to_return.append(denomination)
                remaining -= value
                available -= 1

        return ChangePlan(coins=change_to_return, remaining=remaining)

