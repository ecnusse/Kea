"""
This is the PDL (Property Desciption Language) for Android app testing, which is 
kind of DSL(Domain Sepcific Language).
Please checkout our doc and paper for details.
"""

from uiautomator2._selector import Selector, UiObject
from uiautomator2 import Device as Driver
from typing import Any, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from kea.droidbot import DroidBot
import time

class PDL(Driver):
    droidbot = None    

    def __init__(self, delay=1) -> None:
        self.delay = delay

    def set_device_serial(self, serial):
        super().__init__(serial=serial)
        # setting operation delay
        self.settings['operation_delay'] = (0, self.delay)
        self.settings['wait_timeout'] = 5.0 # 默认控件等待时间

    def __call__(self, **kwargs: Any) -> "Ui":
        return Ui(self, Selector(**kwargs), droidbot=self.droidbot)

    def set_droidbot(self, droidbot:"DroidBot"):
        self.droidbot = droidbot

    def rotate(self, mode: str):
        self.droidbot.device.save_screenshot_for_report(event_name="rotate", event = self)
        super().set_orientation(mode)
        time.sleep(1)

    def press(self, key: Union[int, str], meta=None):
        self.droidbot.device.save_screenshot_for_report(event_name="press", event = key)
        super().press(key, meta)


class Ui(UiObject):
    def __init__(self, session:"PDL", selector: Selector, droidbot:"DroidBot"):
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
        return Ui(self.session, self.selector.clone().child(**kwargs))
    
    def sibling(self, **kwargs):
        return Ui(self.session, self.selector.clone().sibling(**kwargs))