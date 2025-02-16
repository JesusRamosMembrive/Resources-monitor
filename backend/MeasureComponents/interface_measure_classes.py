from abc import ABC, abstractmethod

class iMeasure(ABC):
    @abstractmethod
    def collect_data(self):
        pass