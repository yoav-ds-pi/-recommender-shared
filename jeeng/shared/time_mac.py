from dataclasses import dataclass
from time import time


@dataclass(frozen=True)
class TimerResult:
    name: str
    delta: float

    def __str__(self):
        return f'{self.name}={self.delta:.3f}'


@dataclass
class Timer:
    name: str
    start: float

    def __init__(self, name: str):
        self.name = name
        self.start = time()

    def stop(self):
        return TimerResult(name=self.name, delta=time() - self.start)
