from src.domain.coins import Coins
from src.domain.product import Product
from src.domain.vending_machine import VendingMachine


def main():
    products = [
        Product(name="Cola", amount=5, price=150),
        Product(name="Crisps", amount=3, price=75),
        Product(name="Water", amount=10, price=50),
    ]

    change = [
        Coins(denomination="1p", quantity=20),
        Coins(denomination="2p", quantity=20),
        Coins(denomination="5p", quantity=20),
        Coins(denomination="10p", quantity=20),
        Coins(denomination="20p", quantity=20),
        Coins(denomination="50p", quantity=10),
        Coins(denomination="£1", quantity=10),
        Coins(denomination="£2", quantity=5),
    ]

    machine = VendingMachine(products=products, change=change)

    machine.insert_coin("£1")
    machine.insert_coin("50p")
    machine.select_product("Cola")


if __name__ == "__main__":
    main()
