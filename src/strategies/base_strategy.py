from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    def __init__(self, data, capital):
        self.data = data
        self.capital = capital
        self.positions = []

    @abstractmethod
    def generate_signals(self):
        """Generate buy/sell signals based on the strategy."""
        pass
