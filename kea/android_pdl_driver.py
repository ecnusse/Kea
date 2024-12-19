"""
This is the PDL (Property Desciption Language) for Android, which is one 
kind of DSL (Domain Sepcific Language). 
Please checkout Kea's doc and its paper for the details.
"""

from uiautomator2._selector import Selector, UiObject
from uiautomator2 import Device as Driver
from typing import Any, Union, TYPE_CHECKING
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
    def __init__(self, session:"Android_PDL_Driver", selector: Selector, droidbot:"DroidBot"):
        super().__init__(session, selector)
        self.droidbot=droidbot

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