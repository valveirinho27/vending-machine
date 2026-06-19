import pytest

from src.models.coins import Coins
from src.models.product import Product
from src.vending_machine import VendingMachine


def _build_machine(products=None, change=None) -> VendingMachine:
    default_products = [Product(name="Cola", amount=2, price=150)]
    default_change = [
        Coins("1p", 10),
        Coins("2p", 10),
        Coins("5p", 10),
        Coins("10p", 10),
        Coins("20p", 10),
        Coins("50p", 10),
        Coins("£1", 10),
        Coins("£2", 10),
    ]
    return VendingMachine(products or default_products, change or default_change)


def test_insert_coin_updates_current() -> None:
    machine = _build_machine()

    machine.insert_coin("£1")
    machine.insert_coin("50p")

    assert machine.current == 150


def test_insert_coin_rejects_unknown_coin() -> None:
    machine = _build_machine()

    with pytest.raises(ValueError):
        machine.insert_coin("3p")


def test_reload_change_adds_to_existing_quantity_and_new_denomination() -> None:
    machine = _build_machine(change=[Coins("1p", 2)])

    machine.reload_change([Coins("1p", 3), Coins("2p", 4)])

    assert machine.change["1p"] == 5
    assert machine.change["2p"] == 4


def test_reload_products_updates_existing_stock_and_adds_new_product() -> None:
    machine = _build_machine(products=[Product(name="Cola", amount=2, price=150)])

    machine.reload_products([
        Product(name="Cola", amount=3, price=150),
        Product(name="Water", amount=5, price=50),
    ])

    assert machine.products["Cola"].amount == 5
    assert machine.products["Water"].amount == 5


def test_select_product_dispenses_and_decrements_stock(capsys) -> None:
    machine = _build_machine(products=[Product(name="Cola", amount=2, price=150)])
    machine.current = 150

    machine.select_product("Cola")

    out = capsys.readouterr().out
    assert "Dispensing Cola." in out
    assert machine.products["Cola"].amount == 1
    assert machine.current == 0


def test_select_product_with_insufficient_funds_keeps_state(capsys) -> None:
    machine = _build_machine(products=[Product(name="Cola", amount=2, price=150)])
    machine.current = 100

    machine.select_product("Cola")

    out = capsys.readouterr().out
    assert "Not enough money inserted." in out
    assert machine.products["Cola"].amount == 2
    assert machine.current == 100


def test_select_product_refuses_purchase_when_exact_change_is_unavailable(capsys) -> None:
    machine = _build_machine(
        products=[Product(name="Cola", amount=1, price=145)],
        change=[Coins("2p", 2)],
    )
    machine.current = 150

    machine.select_product("Cola")

    out = capsys.readouterr().out
    assert "Unable to dispense product because exact change is not available." in out
    assert machine.products["Cola"].amount == 1
    assert machine.current == 150


def test_return_change_uses_best_combination_without_overshoot(capsys) -> None:
    machine = _build_machine(change=[Coins("2p", 2), Coins("1p", 1)])
    machine.current = 3

    machine.return_change()

    out = capsys.readouterr().out
    assert "Returning change: 2p, 1p." in out
    assert machine.change["2p"] == 1
    assert machine.change["1p"] == 0
    assert machine.current == 0


def test_return_change_returns_partial_and_warns_when_exact_not_possible(capsys) -> None:
    machine = _build_machine(change=[Coins("2p", 2)])
    machine.current = 150

    machine.return_change()

    out = capsys.readouterr().out
    assert "Returning change: 2p, 2p." in out
    assert "Warning: Unable to return exact change." in out
    assert machine.change["2p"] == 0
    assert machine.current == 0

