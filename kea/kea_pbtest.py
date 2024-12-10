import attr
import inspect
from typing import TYPE_CHECKING, List
from .utils import INITIALIZER_MARKER, MAINPATH_MARKER, RULE_MARKER
if TYPE_CHECKING:
    from kea.kea import Kea

@attr.s()
class Rule:    # tingsu: what does these mean, including Rule, MainPath, initializer, precondition?
    """
    A rule corresponds to a property (including precondition, interaction scenario, postconditions)
    """
    
    # `preconditions` denotes the preconditions annotated with `@precondition`
    preconditions = attr.ib()  # TODO rename `preconditions` to `precondition`?

    # `function` denotes the function of @Rule. This function includes the interaction scenario and the assertions (i.e., the postconditions) therein
    # TODO we may need to rename `function` to `method`?
    function = attr.ib()

    def __str__(self) -> str:
        return f"Rule(function: {self.function.__qualname__})"

@attr.s()
class MainPath:
    
    # `function` denotes the function of `@mainPath.
    function = attr.ib()

    # the interaction steps in the main path
    path: List[str] = attr.ib()  # TODO rename `path` to a more suitable name?


@attr.s()
class Initializer:
    
    # `function` denotes the function of `@initializer.
    function = attr.ib()


class KeaPBTest: 
    rule_list:List["Rule"] = list()
    initializer_list:List["Rule"] = list() # TODO why  "Rule"?
    mainPath_list:List["MainPath"] = list()

    def get_list(self, MARKER:str, kea_test_class:"Kea"):
        """
        Dynamically get the rule/initializer/mainPath list from the testCase.
        """

        mapping = {INITIALIZER_MARKER:"initializer_list",
                   MAINPATH_MARKER:"mainPath_list",
                   RULE_MARKER:"rule_list"}
        TARGET_LIST_NAME = mapping[MARKER]

        # Else, initialize the list 
        # (TestCase is singleton so the other initialized lists won't be covered)
        setattr(self, TARGET_LIST_NAME, [])
        for _, v in inspect.getmembers(kea_test_class):
            r = getattr(v, MARKER, None)
            if r is not None:
                getattr(self, TARGET_LIST_NAME).append(r)
        return getattr(self, TARGET_LIST_NAME)