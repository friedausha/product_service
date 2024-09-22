import threading
import time


class Cache:
    def __init__(self):
        self.cache = {}
        self.ttl = {}
        self.lock = threading.Lock()

    def get_key(self, key):
        # return self.cache.get(key, None)
        with self.lock:
            if key in self.ttl and time.time() > self.ttl[key]:
                self.time(key)
            return self.cache.get(key)

    def set(self, key, value, ttl=None):
        # self.cache[key] = value
        with self.lock:
            self.cache[key] = value
            if ttl:
                self.ttl[key] = time.time() + ttl

    def time(self, key):
        self.cache.pop(key, None)

cache = Cache()