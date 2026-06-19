from src.constants import COIN_DENOMINATIONS
from src.domain.coins import Coins
from src.domain.product import Product
from src.services.change_maker import ChangeMaker
from src.utils.formatting import pence_to_string


class VendingMachine:
    def __init__(self, products: list[Product], change: list[Coins]) -> None:
        self.products: dict[str, Product] = {p.name: p for p in products}
        self.change: dict[str, int] = {c.denomination: c.quantity for c in change}
        self.current: int = 0

    def reload_change(self, change: list[Coins]) -> None:
        for coin in change:
            if coin.denomination in self.change:
                self.change[coin.denomination] += coin.quantity
            else:
                self.change[coin.denomination] = coin.quantity

    def reload_products(self, products: list[Product]) -> None:
        for product in products:
            if product.name in self.products:
                self.products[product.name].amount += product.amount
            else:
                self.products[product.name] = product

    def insert_coin(self, coin: str) -> None:
        if coin not in COIN_DENOMINATIONS:
            raise ValueError(f"Unrecognised coin: '{coin}'.")
        self.current += COIN_DENOMINATIONS[coin]
        print(f"Inserted {coin}. Total inserted: {pence_to_string(self.current)}.")

    def select_product(self, product_name: str) -> None:
        if product_name not in self.products:
            print(f"Product '{product_name}' does not exist.")
            return

        product = self.products[product_name]

        if product.amount == 0:
            print(f"Sorry, '{product_name}' is out of stock.")
            return

        if self.current < product.price:
            shortfall = product.price - self.current
            print(f"Not enough money inserted. Please insert the remaining: {pence_to_string(shortfall)}.")
            return

        change_due = self.current - product.price
        if change_due > 0:
            change_plan = ChangeMaker.calculate(change_due, self.change)
            if not change_plan.exact:
                print("Unable to dispense product because exact change is not available.")
                return

        self.current -= product.price
        product.amount -= 1
        print(f"Dispensing {product.name}.")
        self.return_change()

    def return_change(self) -> None:
        if self.current == 0:
            return

        change_plan = ChangeMaker.calculate(self.current, self.change)

        for denomination in change_plan.coins:
            self.change[denomination] -= 1

        self.current = 0

        if change_plan.coins:
            print(f"Returning change: {', '.join(change_plan.coins)}.")

        if not change_plan.exact:
            print(f"Warning: Unable to return exact change. Missing {pence_to_string(change_plan.remaining)}.")

