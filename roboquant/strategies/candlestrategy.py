from abc import abstractmethod, ABC
from typing import Dict

from roboquant.event import Candle
from roboquant.signal import Signal
from roboquant.strategies.buffer import OHLCVBuffer
from roboquant.strategies.strategy import Strategy


class CandleStrategy(Strategy, ABC):
    """Abstract base class for other strategies that helps to implement trading solutions
    based on technical indicators using candles.
    """

    def __init__(self, size: int) -> None:
        super().__init__()
        self._data: Dict[str, OHLCVBuffer] = {}
        self.size = size

    def create_signals(self, event) -> Dict[str, Signal]:
        signals = {}
        for item in event.items:
            if isinstance(item, Candle):
                symbol = item.symbol
                if symbol not in self._data:
                    self._data[symbol] = OHLCVBuffer(self.size)
                ohlcv = self._data[symbol]
                ohlcv.append(item.ohlcv)
                if ohlcv.is_full():
                    signal = self._create_signal(symbol, ohlcv)
                    if signal is not None:
                        signals[symbol] = signal
        return signals

    @abstractmethod
    def _create_signal(self, symbol: str, ohlcv: OHLCVBuffer) -> Signal | None:
        """
        Subclasses should implement this method and return a signal or None for the provided symbol and ohlcv data.
        """
        ...
