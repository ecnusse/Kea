import random
import string

from hypothesis import strategies as st

class Bundle():
    def __init__(self, type: str = None) -> None:
        self.type = type
        self.data = []

    def add(self, value = None):
        if value is None:
            raise ValueError("the value of " + self.type + " cannot be None")
        self.data.append(value)
        print(self.type, self.data)

    def delete(self, value = None):
        if value is None:
            raise ValueError("the value of " + self.type + " cannot be None")
        self.data.remove(value)
        print(self.type, self.data)

    def update(self, value = None, new_value = None):
        if new_value is None:
            raise ValueError("the new name of " + self.type + " cannot be None")
        if value is None:
            raise ValueError("the old name of " + self.type + " cannot be None")
        try:
            self.data.remove(value)
            self.data.append(new_value)
        except KeyError:
            print(f"'{value}' is not a object of Bundle.")
        print(self.type, self.data)

    def get_all_data(self):
        return self.data

    def get_random_value(self, value_len = 10):
        value = st.text(alphabet=string.ascii_letters, min_size=1, max_size=value_len).example()
        return value

    def get_random_data(self):
        random_item = random.choice(self.data)
        return random_item
