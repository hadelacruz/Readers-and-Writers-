# semaphore_custom.py
import threading

class Semaphore:
    def __init__(self, initial):
        self.value = initial
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)

    def wait(self):
        with self.lock:
            while self.value <= 0:
                self.condition.wait()
            self.value -= 1

    def signal(self):
        with self.lock:
            self.value += 1
            self.condition.notify()