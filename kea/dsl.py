from uiautomator2._selector import Selector, UiObject
from uiautomator2 import Device
import time
from typing import Any, Union

class Mobile(Device):
    
    def __init__(self, delay=1) -> None:
        
        self.delay = delay

    def set_device_serial(self, serial):
        super().__init__(serial=serial)
        # setting operation delay
        self.settings['operation_delay'] = (0, self.delay)
        self.settings['wait_timeout'] = 5.0 # 默认控件等待时间
    def __call__(self, **kwargs: Any) -> Any:
        return Ui(self, Selector(**kwargs))

    def set_droidbot(self, droidbot):
        self.droidbot = droidbot

    def rotate(self, mode: str):
        super().set_orientation(mode)
        self.droidbot.device.take_screenshot(True, "rotate")

    def press(self, key: Union[int, str], meta=None):
        super().press(key, meta)
        self.droidbot.device.take_screenshot(True, "press")


class Ui(UiObject):

    def click(self, offset=None):
        super().click(offset)
        self.session.droidbot.device.take_screenshot(True, "click")

    def long_click(self, duration: float = 0.5):
        super().long_click(duration)
        self.session.droidbot.device.take_screenshot(True, "long_click")
    
    def set_text(self, text):
        super().set_text(text)
        self.session.droidbot.device.take_screenshot(True, "set_text "+text)
        
    def child(self, **kwargs):
        return Ui(self.session, self.selector.clone().child(**kwargs))
    
    def sibling(self, **kwargs):
        return Ui(self.session, self.selector.clone().sibling(**kwargs))