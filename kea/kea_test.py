import inspect
import attr
from typing import Callable, Any, Union, TYPE_CHECKING, Dict
from .kea import Rule, MainPath, Initializer
from .Bundle import Bundle
from .utils import PRECONDITIONS_MARKER, RULE_MARKER, INITIALIZER_MARKER, MAINPATH_MARKER

if TYPE_CHECKING:
    from .pdl import PDL as Android_PDL
    from .pdl_hm import PDL as HarmonyOS_PDL
    from .kea import Rule, MainPath

class KeaTest:
    pass


# `d` is the pdl driver for Android or HarmonyOS
d:Union["Android_PDL", "HarmonyOS_PDL", None] = None

def rule() -> Callable:
    def accept(f):
        precondition = getattr(f, PRECONDITIONS_MARKER, ())
        rule = Rule(function=f, preconditions=precondition)

        def rule_wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        setattr(rule_wrapper, RULE_MARKER, rule)
        return rule_wrapper

    return accept


def precondition(precond: Callable[[Any], bool]) -> Callable:
    def accept(f):
        def precondition_wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        rule:"Rule" = getattr(f, RULE_MARKER, None)
        if rule is not None:
            new_rule = rule.evolve(preconditions=rule.preconditions + (precond,))
            # new_rule = attr.evolve(rule, preconditions=rule.preconditions + (precond,))
            setattr(precondition_wrapper, RULE_MARKER, new_rule)
        else:
            setattr(
                precondition_wrapper,
                PRECONDITIONS_MARKER,
                getattr(f, PRECONDITIONS_MARKER, ()) + (precond,),
            )
        return precondition_wrapper

    return accept

def initializer():
    '''
    An initialize decorator behaves like a rule, but all ``@initialize()`` decorated
    methods will be called before any ``@rule()`` decorated methods, in an arbitrary
    order.  Each ``@initialize()`` method will be called exactly once per run, unless
    one raises an exception.
    '''

    def accept(f):
        def initialize_wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        initializer_func = Initializer(function=f)
        #rule = Rule(function=f, preconditions=())
        setattr(initialize_wrapper, INITIALIZER_MARKER, initializer_func)
        return initialize_wrapper

    return accept

def mainPath():
    def accept(f):
        def mainpath_wrapper(*args, **kwargs):
            source_code = inspect.getsource(f)
            code_lines = [line.strip() for line in source_code.splitlines() if line.strip()]
            code_lines = [line for line in code_lines if not line.startswith('def ') and not line.startswith('@') and not line.startswith('#')]
            return code_lines

        main_path = MainPath(function=f, path=mainpath_wrapper())
        setattr(mainpath_wrapper, MAINPATH_MARKER, main_path)
        return mainpath_wrapper

    return accept