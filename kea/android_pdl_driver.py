"""
This is the PDL (Property Desciption Language) for Android, which is one 
kind of DSL (Domain Sepcific Language). 
Please checkout Kea's doc and its paper for the details.
"""

from deprecated import deprecated
from uiautomator2._selector import Selector, UiObject
from uiautomator2 import Device as Driver
from typing import Any, Union, TYPE_CHECKING, Dict
import ast
import random
if TYPE_CHECKING:
    from kea.droidbot import DroidBot
import time

class Android_PDL_Driver(Driver):
    """The pdl driver for Android
    """

    droidbot = None    

    def __init__(self, serial, delay=1) -> None:
        super().__init__(serial=serial)
        self.delay = delay
        # set the delay between sending events
        self.settings['operation_delay'] = (0, self.delay)
        # default timeout for waiting a widget to appear.
        self.settings['wait_timeout'] = 5.0  

    def __call__(self, **kwargs: Any) -> "Ui":
        return Ui(self, Selector(**kwargs), droidbot=self.droidbot)

    def set_droidbot(self, droidbot:"DroidBot"):
        self.droidbot = droidbot

    def rotate(self, mode: str):  # TODO: what does mode mean? why "rotate"/"press" not included in the Ui class
        """

        """
        self.droidbot.device.save_screenshot_for_report(event_name="rotate", event = self)
        super().set_orientation(mode)
        time.sleep(1)

    def press(self, key: Union[int, str], meta=None): # TODO: what does meta mean?
        """
            key: home, back, menu, search, recent
            meta: 
        """
        self.droidbot.device.save_screenshot_for_report(event_name="press", event = key)
        super().press(key, meta)


class Ui(UiObject):
    """
    TODO extend more UI operations, e.g., random selecting one tag
    """
    def __init__(self, 
                 session:"Android_PDL_Driver",
                 selector: Selector,
                 droidbot:"DroidBot"):
        super().__init__(session, selector)
        self.droidbot=droidbot
        self.selector=selector
    
    def exists(self):
        # TODO add a static checker here
        cur_state = self.droidbot.device.from_state
        kwargs = dict()
        for key, value in self.selector.items():
            if key not in ["mask", "childOrSibling", "childOrSiblingSelector"]:
                kwargs[key] = value
        view = cur_state.get_view_by_attribute(kwargs)
        return view is not None

    def click(self, offset=None):
        self.droidbot.device.save_screenshot_for_report(event_name="click", event = self)
        print(f"Property Action: click({str(self.selector)})")
        super().click(offset)

    def long_click(self, duration: float = 0.5):
        self.droidbot.device.save_screenshot_for_report(event_name="long_click",  event = self)
        print(f"Property Action: long_click({str(self.selector)})")
        super().long_click(duration)
    
    def set_text(self, text):
        self.droidbot.device.save_screenshot_for_report(event_name="set_text " + text, event = self)
        print(f"Property Action: set_text({str(self.selector)})")
        super().set_text(text)
        
    def child(self, **kwargs):
        return Ui(self.session, self.selector.clone().child(**kwargs), self.droidbot)
    
    def sibling(self, **kwargs):
        return Ui(self.session, self.selector.clone().sibling(**kwargs), self.droidbot)


class PDLScriptParser:
    """
    This class is used for parsering a pdl script with AST
    A pdl script is "d(Selector(**kwargs)).method()"
    The parsed pdl script can be used in precondition checker, mainpath ...
    This class will transform the script to AST
    """
    def __init__(self, exec_script):
        self.ast_tree = ast.parse(exec_script)
        # self.print_tree()
        self._ui_attribute: Dict[str, Dict[str, str]] = None
    
    def print_tree(self):
        print(ast.dump(self.ast_tree, indent=4))
    
    def parse_device_args(self, ast_tree: ast.AST) -> Dict[str, Dict[str, str]]:
        ui_attribute_getter = UIAttributeGetter()
        ui_attribute_getter.visit(ast_tree)
        # print(ui_attribute_getter.ui_attribute)
        return ui_attribute_getter.ui_attribute
    
    # @deprecated("This funciton is not used yet")
    @property
    def ui_attribute(self):
        """
        ### ui_attribute is the Selector and its call method. Parsed from the source code.
        
        #### Example 1 
        source code: d(resource_id="**", text="**").click()
        
        ui_attribute: {"click": {resouce_id="**", text="**"}}

        #### Example 2
        source code: random.choice(d(resource_id="**", text="**"))
        
        ui_attribute: {"selector": {resouce_id="**", text="**"}}
        """
        if self._ui_attribute is not None:
            return self._ui_attribute
        else:
            self._ui_attribute = self.parse_device_args(self.ast_tree)
            return self.ui_attribute


class UIAttributeGetter(ast.NodeVisitor):
    """
    This class inherits from ast.NodeVisitor, which is used to customize the
    behaviour while visiting an AST to capture the target args.
    """
    def __init__(self):
        super().__init__()
        self.ui_attribute: Dict[str, Dict[str, str]] = dict()
        
    def visit_Call(self, node):
        """
        rewrite the visit_Call method of the ast.NodeVisitor to capture
        the Selector and method of the PDL driver call.
        """

        #! Case 1: parse "d(Selector(**args)).method()"
        # The form should be a nested call
        # Check if it is a nested call
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Call):
            # Get the innermost function name, it should be driver "d"
            if isinstance(node.func.value.func, ast.Name) and \
            (inner_func_name := node.func.value.func.id) == "d":

                selector_args = dict()
                
                # Extract keyword arguments
                for keyword in node.func.value.keywords:
                    key, value = keyword.arg, keyword.value.value
                    selector_args[key] = value
                    
                # Get the outer attribute name, it's the method call. 
                # (e.g. click, exists)
                method = (outer_func_name := node.func.attr)
                self.ui_attribute[method] = selector_args
        
        #! Case 2: parse "d(Selector(**args))"
        # Get the function name, it should be driver "d"
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and \
                node.func.id == "d":
                    
                selector_args = dict()
                
                # Extract keyword arguments
                for keyword in node.keywords:
                    key, value = keyword.arg, keyword.value.value
                    selector_args[key] = value
                
                # remove the duplicated items. Because case 2 is the subset
                # of case 1. If already included in case 1, don't add in case 2.
                if selector_args not in list(self.ui_attribute.values()):
                    self.ui_attribute["selector"] = selector_args

        # Continue traversing child nodes
        self.generic_visit(node)


if __name__ == "__main__":
    # script = """random.choice(d(resourceId="it.feio.android.omninotes.alpha:id/done", text="Hello World"))"""
    script = """d(resourceId="it.feio.android.omninotes.alpha:id/done", text="Hello World").exists()"""

    pdl_parser = PDLScriptParser(script)
    print(pdl_parser.ui_attribute)
