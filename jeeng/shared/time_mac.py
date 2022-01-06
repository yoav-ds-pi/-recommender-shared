from dataclasses import dataclass
from datetime import timedelta
from time import time


@dataclass(frozen=True)
class TimerResult:
    name: str
    delta: timedelta

    def __str__(self):
        return f'{self.name}={self.delta}'


@dataclass
class Timer:
    name: str
    start: float

    def __init__(self, name: str):
        self.name = name
        self.start = time()

    def stop(self):
        return TimerResult(name=self.name, delta=timedelta(seconds=time()-self.start))

    def stop_round(self):
        return TimerResult(name=self.name, delta=timedelta(seconds=round(time()-self.start)))

