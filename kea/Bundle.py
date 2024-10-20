import random
import string

from hypothesis import strategies as st

class Bundle():
    def __init__(self, type: str = None) -> None:
        self.type = type
        self.data = []

    def add_data(self, name = None):
        if name is None:
            raise ValueError("the value of " + self.type + " cannot be None")
        self.data.append(name)
        print(self.type, self.data)

    def del_data(self, name = None):
        if name is None:
            raise ValueError("the value of " + self.type + " cannot be None")
        self.data.remove(name)
        print(self.type, self.data)

    def update_data(self, name = None, value = None):
        if value is None:
            raise ValueError("the new name of " + self.type + " cannot be None")
        if name is None:
            raise ValueError("the old name of " + self.type + " cannot be None")
        try:
            self.data.remove(name)
            self.data.append(value)
        except KeyError:
            print(f"'{name}' is not a object of Bundle.")
        print(self.type, self.data)

    def get_all_data(self):
        return self.data

    def get_random_name(self, name_len = 10):
        name = st.text(alphabet=string.ascii_letters, min_size=1, max_size=name_len).example()
        return name

    def get_random_data(self):
        random_item = random.choice(self.data)
        return random_item
