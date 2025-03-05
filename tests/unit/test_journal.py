import pathlib
import unittest
# from matplotlib import pyplot as plt

from roboquant.feeds import CSVFeed
from roboquant.journals import RunMetric
from roboquant.strategies.emacrossover import EMACrossover
from roboquant import run
from roboquant.journals.plotjournal import PlotJournal



class TestJournal(unittest.TestCase):

    @staticmethod
    def _get_root_dir(*paths):
        root = pathlib.Path(__file__).parent.resolve().joinpath("..", "data", *paths)
        return str(root)

    def test_plotjournal(self):
        root = self._get_root_dir("yahoo")
        feed = CSVFeed.yahoo(root)
        apple = feed.get_asset("AAPL")
        strategy = EMACrossover()
        journal = PlotJournal(apple, RunMetric())

        run(feed, strategy, journal=journal)
        journal.plot()
        # plt.show()


if __name__ == "__main__":
    unittest.main()
