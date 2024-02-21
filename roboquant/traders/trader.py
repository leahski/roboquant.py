from typing import Protocol
from roboquant.account import Account
from roboquant.event import Event
from roboquant.order import Order
from roboquant.signal import Signal


class Trader(Protocol):
    """A trader generates the orders, typically based on signals it receives from a strategy.

    But it is also possible to implement all logic in a Trader and don't rely on signals generated by a strategy at all.
    """

    def create_orders(self, signals: dict[str, Signal], event: Event, account: Account) -> list[Order]:
        """Create zero or more orders."""
        ...
