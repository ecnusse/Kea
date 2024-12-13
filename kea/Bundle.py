import random
import string
from typing import Dict

from hypothesis import strategies as st

class Bundle():
    def __init__(self, data_name: str = None) -> None:
        """
        Initialize a Bundle. 
        """
        self.data_name = data_name
        self.data_value = []

    def __new__(cls, data_name: str = None):
        return super().__new__(cls)

    def add(self, value = None):
        if value is None:
            raise ValueError("the value of " + self.data_name + " cannot be None")
        self.data_value.append(value)
        print(self.data_name, self.data_value)

    def delete(self, value = None):
        if value is None:
            raise ValueError("the value of " + self.data_name + " cannot be None")
        self.data_value.remove(value)
        print(self.data_name, self.data_value)

    def update(self, value = None, new_value = None):
        if new_value is None:
            raise ValueError("the new name of " + self.data_name + " cannot be None")
        if value is None:
            raise ValueError("the old name of " + self.data_name + " cannot be None")
        try:
            self.data_value.remove(value)
            self.data_value.append(new_value)
        except KeyError:
            print(f"'{value}' is not a object of Bundle.")
        print(self.data_name, self.data_value)

    def get_all_data(self):
        return self.data_value

    def get_random_value(self, value_len = 10):
        value = st.text(alphabet=string.ascii_letters, min_size=1, max_size=value_len).example()
        return value

    def get_random_data(self):
        random_item = random.choice(self.data_value)
        return random_item

class PublicBundle(Bundle):
    _bundles_: Dict[str, "Bundle"] = {}
    def __init__(self, data_name: str = None) -> None:
        """
        Initialize a PublicBundle.
        """
        super().__init__(data_name)

    def __new__(cls, data_name: str = None):
        if data_name in cls._bundles_:
            return cls._bundles_[data_name]
        else:
            instance = super().__new__(cls)
            cls._bundles_[data_name] = instance
            return instance