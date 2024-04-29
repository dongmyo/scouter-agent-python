class BackgroundContext:
    def __init__(self):
        self.cancelled = False
        self.values = {}

    def cancel(self):
        self.cancelled = True

    def is_cancelled(self):
        return self.cancelled

    def get_value(self, key):
        return self.values.get(key, None)

    def set_value(self, key, value):
        self.values[key] = value
