import random
import string

from hypothesis import strategies as st

class Bundle():
    def __init__(self, type: str = None) -> None:
        self.type = type
        self.data = []

    def add(self, test = None):
        if test is None:
            raise ValueError("the value of " + self.type + " cannot be None")
        self.data.append(test)
        print(self.type, self.data)

    def delete(self, test = None):
        if test is None:
            raise ValueError("the value of " + self.type + " cannot be None")
        self.data.remove(test)
        print(self.type, self.data)

    def update(self, test = None, value = None):
        if value is None:
            raise ValueError("the new name of " + self.type + " cannot be None")
        if test is None:
            raise ValueError("the old name of " + self.type + " cannot be None")
        try:
            self.data.remove(test)
            self.data.append(value)
        except KeyError:
            print(f"'{test}' is not a object of Bundle.")
        print(self.type, self.data)

    def get_all_data(self):
        return self.data

    def get_random_test(self, test_len = 10):
        test = st.text(alphabet=string.ascii_letters, min_size=1, max_size=test_len).example()
        return test

    def get_random_data(self):
        random_item = random.choice(self.data)
        return random_item
