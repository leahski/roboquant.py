from datetime import datetime
import logging
from roboquant.event import Event
from roboquant.feeds.feed import Feed
from roboquant.signal import Signal
from roboquant.strategies.strategy import Strategy
from roboquant.timeframe import Timeframe

logger = logging.getLogger(__name__)

class CachingStrategy(Strategy):
    """Cache the results of a strategy, usefull for shorter back tests"""

    def __init__(self, feed: Feed, strategy: Strategy, timeframe: Timeframe | None = None):
        super().__init__()
        cache: dict[datetime, list[Signal]] = {}
        for event in feed.play(timeframe):
            assert event.time not in cache, "feed has to be monotonic in time"
            signals = strategy.create_signals(event)
            cache[event.time] = signals
        self.__cache = cache

    def create_signals(self, event: Event) -> list[Signal]:
        result = self.__cache.get(event.time)
        if result is None:
            logging.warning("received unknown timestamp %s, returning no signals", event.time)
            return []
        return result

