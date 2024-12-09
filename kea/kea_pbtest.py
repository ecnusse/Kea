import attr
import inspect
from typing import TYPE_CHECKING, List
from .utils import INITIALIZER_MARKER, MAINPATH_MARKER, RULE_MARKER
if TYPE_CHECKING:
    from kea.kea import Kea

@attr.s()
class Rule:    # tingsu: what does these mean, including Rule, MainPath, initializer, precondition?
    function = attr.ib()
    preconditions = attr.ib()

    def __str__(self) -> str:
        return f"Rule(function: {self.function.__qualname__})"

@attr.s()
class MainPath:
    function = attr.ib()
    path = attr.ib()


class KeaPBTest: 
    rule_list:List["Rule"]
    initializer_list:List["Rule"]
    mainPath_list:List["MainPath"]

    def get_list(self, MARKER:str, kea_test_class:"Kea"):
        """
        Dynamically get the rule/initializer/mainPath list from the testCase.
        """

        mapping = {INITIALIZER_MARKER:"initializer_list",
                   MAINPATH_MARKER:"mainPath_list",
                   RULE_MARKER:"rule_list"}
        TARGET_LIST_NAME = mapping[MARKER]

        # return the list if it has already been initialized
        if hasattr(self, TARGET_LIST_NAME):
            return getattr(self, TARGET_LIST_NAME)

        # Else, initialize the list 
        # (TestCase is singleton so the other initialized lists won't be covered)
        setattr(self, TARGET_LIST_NAME, [])
        for _, v in inspect.getmembers(kea_test_class):
            r = getattr(v, MARKER, None)
            if r is not None:
                getattr(self, TARGET_LIST_NAME).append(r)
        return getattr(self, TARGET_LIST_NAME)