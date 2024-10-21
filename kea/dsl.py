from uiautomator2._selector import Selector, UiObject
from uiautomator2 import Device
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
        self.droidbot.device.take_screenshot(True, "rotate")
        super().set_orientation(mode)

    def press(self, key: Union[int, str], meta=None):
        self.droidbot.device.take_screenshot(True, "press")
        super().press(key, meta)


class Ui(UiObject):

    def click(self, offset=None):
        self.session.droidbot.device.take_screenshot(True, "click")
        super().click(offset)

    def long_click(self, duration: float = 0.5):
        self.session.droidbot.device.take_screenshot(True, "long_click")
        super().long_click(duration)
    
    def set_text(self, text):
        self.session.droidbot.device.take_screenshot(True, "set_text " + text)
        super().set_text(text)
        
    def child(self, **kwargs):
        return Ui(self.session, self.selector.clone().child(**kwargs))
    
    def sibling(self, **kwargs):
        return Ui(self.session, self.selector.clone().sibling(**kwargs))