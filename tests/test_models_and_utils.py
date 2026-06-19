import pytest

from src.models.coins import Coins
from src.models.product import Product
from src.utils import pence_to_string


def test_coins_validation_rejects_invalid_denomination() -> None:
    with pytest.raises(ValueError):
        Coins("3p", 1)


def test_coins_validation_rejects_negative_quantity() -> None:
    with pytest.raises(ValueError):
        Coins("1p", -1)


def test_product_validation_rejects_invalid_values() -> None:
    with pytest.raises(ValueError):
        Product(name="Cola", amount=1, price=0)
    with pytest.raises(ValueError):
        Product(name="Cola", amount=-1, price=100)


def test_pence_to_string_formats_values() -> None:
    assert pence_to_string(0) == "0p"
    assert pence_to_string(99) == "99p"
    assert pence_to_string(100) == "£1"
    assert pence_to_string(150) == "£1.50"

