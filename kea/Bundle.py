import random
import string

from hypothesis import strategies as st

class Bundle():
    def __init__(self, type: str = None) -> None:
        self.type = type
        self.data = []

    def add_data(self, name = None):
        if name is None:
            name = st.text(alphabet=string.ascii_letters,min_size=1, max_size=10).example()
        self.data.append(name)
        return name

    def del_data(self, name = None):
        if name is None:
            random_item = random.choice(self.data)
            name = random_item
        self.data.remove(name)
        return name

    def update_data(self, name = None, value = None):
        if value is None:
            value = st.text(alphabet=string.ascii_letters,min_size=1, max_size=10).example()
        if name is None:
            random_item = random.choice(self.data)
            name = random_item
        try:
            self.data.remove(name)
            self.data.append(value)
        except KeyError:
            print(f"'{name}' is not a object of Bundle.")
        return name, value

    def get_all_data(self):
        return self.data

