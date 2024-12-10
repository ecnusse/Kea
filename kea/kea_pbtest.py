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

    def load_rule_list(self, kea_test_class:"Kea"):
        """
        Load the rule from the kea_test_class (user written property).
        """
        for _, v in inspect.getmembers(kea_test_class):
            rule = getattr(v, RULE_MARKER, None)
            if rule is not None:
                self.rule_list.append(rule)
        return self.rule_list

    def load_initializer_list(self, kea_test_class:"Kea"):
        """
        Load the rule from the kea_test_class (user written property).
        """
        for _, v in inspect.getmembers(kea_test_class):
            initializer = getattr(v, INITIALIZER_MARKER, None)
            if initializer is not None:
                self.initializer_list.append(initializer)
        return self.initializer_list

    def load_mainPath_list(self, kea_test_class:"Kea"):
        """
        Load the rule from the kea_test_class (user written property).
        """
        for _, v in inspect.getmembers(kea_test_class):
            mainPath = getattr(v, MAINPATH_MARKER, None)
            if mainPath is not None:
                self.mainPath_list.append(mainPath)
        return self.mainPath_list 