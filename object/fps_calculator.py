from math import inf
from time import time, sleep

from object import Object


class FPSCalculator(Object):
    def __init__(self):
        super().__init__(0, 0)

        self.fps: float = 0.0
        self.previous_time = time()

    def tick(self):
        now = time()
        if (duration := 1/70 - (now - self.previous_time)) > 0:
            sleep(duration)
        now = time()

        try:
            self.fps = 1 / (now - self.previous_time)
        except ZeroDivisionError:
            self.fps = inf

        print(self.fps)

        self.previous_time = now
