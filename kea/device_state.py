import copy
import json
import logging
import math
import os
import random

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .device import Device

from .utils import md5, deprecated
from .input_event import SearchEvent, SetTextAndSearchEvent, TouchEvent, LongTouchEvent, ScrollEvent, SetTextEvent, KeyEvent, UIEvent, SwipeEvent


class DeviceState(object):
    """
    the state of the current device
    """

    def __init__(
        self,
        device:"Device",
        views,
        foreground_activity,
        activity_stack,
        background_services,
        tag=None,
        screenshot_path=None,
    ):
        self.device = device
        self.foreground_activity = foreground_activity
        self.activity_stack = activity_stack if isinstance(activity_stack, list) else []
        self.background_services = background_services
        if tag is None:
            from datetime import datetime

            tag = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        self.tag = tag
        self.screenshot_path = screenshot_path
        if foreground_activity is not None:
            self.views = self.__parse_views(views)
            self.view_tree = {}
            self.__assemble_view_tree(self.view_tree, self.views)
            self.__generate_view_strs()
            self.state_str = self.__get_state_str()
            self.structure_str = self.__get_content_free_state_str()
            self.search_content = self.__get_search_content()
            self.text_representation = self.get_text_representation()
        else:
            self.views = []
            self.view_tree = {}
            self.state_str = "home_page_or_lock_screen"
            self.structure_str = "home_page_or_lock_screen"
            self.search_content = "home_page_or_lock_screen"
            self.text_representation = "home_page_or_lock_screen"
        self.possible_events = None
        self.width = device.get_width(refresh=True)
        self.height = device.get_height(refresh=False)
        self.pagePath = self.__get_pagePath()
        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    def activity_short_name(self):
        return self.foreground_activity.split('.')[-1]

    def to_dict(self):
        state = {
            'tag': self.tag,
            'state_str': self.state_str,
            'state_str_content_free': self.structure_str,
            'foreground_activity': self.foreground_activity,
            'activity_stack': self.activity_stack,
            'background_services': self.background_services,
            'width': self.width,
            'height': self.height,
            'views': self.views,
        }
        return state

    def to_json(self):
        import json

        return json.dumps(self.to_dict(), indent=2)
    
    def __parse_views(self, raw_views):
        views = []
        if not raw_views or len(raw_views) == 0:
            return views

        for view_dict in raw_views:
            # # Simplify resource_id
            # resource_id = view_dict['resource_id']
            # if resource_id is not None and ":" in resource_id:
            #     resource_id = resource_id[(resource_id.find(":") + 1):]
            #     view_dict['resource_id'] = resource_id
            views.append(view_dict)
        return views

    def __assemble_view_tree(self, root_view, views):
        if not len(self.view_tree):  # bootstrap
            if not len(views):
                return
            self.view_tree = copy.deepcopy(views[0])
            self.__assemble_view_tree(self.view_tree, views)
        else:
            children = list(enumerate(root_view["children"]))
            if not len(children):
                return
            for i, j in children:
                root_view["children"][i] = copy.deepcopy(self.views[j])
                self.__assemble_view_tree(root_view["children"][i], views)

    def __generate_view_strs(self):
        for view_dict in self.views:
            self.__get_view_str(view_dict)
            # self.__get_view_structure(view_dict)

    @staticmethod
    def __calculate_depth(views):
        root_view = None
        for view in views:
            if DeviceState.__safe_dict_get(view, 'parent') == -1:
                root_view = view
                break
        DeviceState.__assign_depth(views, root_view, 0)

    @staticmethod
    def __assign_depth(views, view_dict, depth):
        view_dict['depth'] = depth
        for view_id in DeviceState.__safe_dict_get(view_dict, 'children', []):
            DeviceState.__assign_depth(views, views[view_id], depth + 1)
    
    def __get_pagePath(self):
        for view in self.views:
            pagePath = self.__safe_dict_get(view, "pagePath")
            if pagePath:
                return pagePath

    def __get_state_str(self):
        state_str_raw = self.__get_state_str_raw()
        return md5(state_str_raw)

    def __get_state_str_raw(self):
        if self.device.humanoid is not None:
            import json
            from xmlrpc.client import ServerProxy

            proxy = ServerProxy("http://%s/" % self.device.humanoid)
            return proxy.render_view_tree(
                json.dumps(
                    {
                        "view_tree": self.view_tree,
                        "screen_res": [
                            self.device.display_info["width"],
                            self.device.display_info["height"],
                        ],
                    }
                )
            )
        else:
            view_signatures = set()
            for view in self.views:
                if self.device.is_harmonyos:
                    # exclude the com.ohos.sceneboard package in harmonyOS
                    if self.__safe_dict_get(view, "package") == "com.ohos.sceneboard":
                        continue
                view_signature = DeviceState.__get_view_signature(view)
                if view_signature:
                    view_signatures.add(view_signature)
            return "%s{%s}" % (self.foreground_activity, ",".join(sorted(view_signatures)))

    def __get_content_free_state_str(self):
        if self.device.humanoid is not None:
            import json
            from xmlrpc.client import ServerProxy

            proxy = ServerProxy("http://%s/" % self.device.humanoid)
            state_str = proxy.render_content_free_view_tree(
                json.dumps(
                    {
                        "view_tree": self.view_tree,
                        "screen_res": [
                            self.device.display_info["width"],
                            self.device.display_info["height"],
                        ],
                    }
                )
            )
        else:
            view_signatures = set()
            
            if self.activity_short_name == "DeckPicker":
                view_signatures = list()
                for view in self.views:
                    view_signature = DeviceState.__get_content_free_view_signature(view)
                    if view_signature:
                        view_signatures.append(view_signature)
            else:
                for view in self.views:
                    view_signature = DeviceState.__get_content_free_view_signature(view)
                    if view_signature:
                        view_signatures.add(view_signature)
            state_str = "%s{%s}" % (
                self.foreground_activity,
                ",".join(sorted(view_signatures)),
            )
        import hashlib

        return hashlib.md5(state_str.encode('utf-8')).hexdigest()

    def __get_search_content(self):
        """
        get a text for searching the state
        :return: str
        """
        words = [
            ",".join(self.__get_property_from_all_views("resource_id")),
            ",".join(self.__get_property_from_all_views("text")),
        ]
        return "\n".join(words)

    def __get_property_from_all_views(self, property_name):
        """
        get the values of a property from all views
        :return: a list of property values
        """
        property_values = set()
        for view in self.views:
            property_value = DeviceState.__safe_dict_get(view, property_name, None)
            if property_value:
                property_values.add(property_value)
        return property_values

    def draw_event(self, event, screenshot_path):
        import cv2
        image = cv2.imread(screenshot_path)
        if event is not None and screenshot_path is not None:
            if isinstance(event, TouchEvent):
                cv2.rectangle(image, (int(event.view['bounds'][0][0]),int(event.view['bounds'][0][1])),(int(event.view['bounds'][1][0]),int(event.view['bounds'][1][1])), (0, 0, 255), 5)
            elif isinstance(event, LongTouchEvent):
                cv2.rectangle(image, (int(event.view['bounds'][0][0]),int(event.view['bounds'][0][1])),(int(event.view['bounds'][1][0]),int(event.view['bounds'][1][1])), (0, 255, 0), 5)
            elif isinstance(event, SetTextEvent):
                cv2.rectangle(image, (int(event.view['bounds'][0][0]),int(event.view['bounds'][0][1])),(int(event.view['bounds'][1][0]),int(event.view['bounds'][1][1])), (255, 0, 0), 5)
            elif isinstance(event, ScrollEvent):
                cv2.rectangle(image, (int(event.view['bounds'][0][0]),int(event.view['bounds'][0][1])),(int(event.view['bounds'][1][0]),int(event.view['bounds'][1][1])), (255, 255, 0), 5)
            elif isinstance(event, KeyEvent):
                cv2.putText(image,event.name, (100,300), cv2.FONT_HERSHEY_SIMPLEX, 5,(0, 255, 0), 3, cv2.LINE_AA)
            else:
                return
            try:
                cv2.imwrite(screenshot_path, image)
            except Exception as e:
                self.logger.warning(e)    
    def save_view_img(self, view_dict, output_dir=None):
        try:
            if output_dir is None:
                if self.device.output_dir is None:
                    return
                else:
                    output_dir = os.path.join(self.device.output_dir, "views")
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            view_str = view_dict['view_str']
            if not self.device.is_harmonyos:
                if self.device.adapters[self.device.minicap]:
                    view_file_path = "%s/view_%s.jpg" % (output_dir, view_str)
                else:
                    view_file_path = "%s/view_%s.png" % (output_dir, view_str)
            else:
                # HarmonyOS
                view_file_path = "%s/view_%s.jpeg" % (output_dir, view_str)
            if os.path.exists(view_file_path):
                return
            from PIL import Image

            # Load the original image:
            view_bound = view_dict['bounds']
            original_img = Image.open(self.screenshot_path)
            # view bound should be in original image bound
            view_img = original_img.crop(
                (
                    min(original_img.width - 1, max(0, view_bound[0][0])),
                    min(original_img.height - 1, max(0, view_bound[0][1])),
                    min(original_img.width, max(0, view_bound[1][0])),
                    min(original_img.height, max(0, view_bound[1][1])),
                )
            )
            view_img.convert("RGB").save(view_file_path)
        except Exception as e:
            self.device.logger.warning(e)

    def is_different_from(self, another_state):
        """
        compare this state with another
        @param another_state: DeviceState
        @return: boolean, true if this state is different from other_state
        """
        return self.state_str != another_state.state_str

    @staticmethod
    def __get_view_signature(view_dict):
        """
        get the signature of the given view
        @param view_dict: dict, an element of list DeviceState.views
        @return:
        """
        if 'signature' in view_dict:
            return view_dict['signature']

        view_text = DeviceState.__safe_dict_get(view_dict, 'text', "None")
        
        if view_text is None or len(view_text) > 50 or DeviceState.__safe_dict_get(view_dict, 'class', "None") == "android.widget.EditText":
            view_text = "None"

        signature = "[class]%s[resource_id]%s[text]%s[%s,%s,%s]" % (
            DeviceState.__safe_dict_get(view_dict, 'class', "None"),
            DeviceState.__safe_dict_get(view_dict, 'resource_id', "None"),
            view_text,
            DeviceState.__key_if_true(view_dict, 'enabled'),
            DeviceState.__key_if_true(view_dict, 'checked'),
            DeviceState.__key_if_true(view_dict, 'selected'),
        )
        view_dict['signature'] = signature
        return signature

    @staticmethod
    def __get_content_free_view_signature(view_dict):
        """
        get the content-free signature of the given view
        @param view_dict: dict, an element of list DeviceState.views
        @return:
        """
        if 'content_free_signature' in view_dict:
            return view_dict['content_free_signature']
        content_free_signature = "[class]%s[resource_id]%s" % (
            DeviceState.__safe_dict_get(view_dict, 'class', "None"),
            DeviceState.__safe_dict_get(view_dict, 'resource_id', "None"),
        )
        view_dict['content_free_signature'] = content_free_signature
        return content_free_signature

    def __get_view_str(self, view_dict):
        """
        get a string which can represent the given view
        @param view_dict: dict, an element of list DeviceState.views
        @return:
        """
        if 'view_str' in view_dict:
            return view_dict['view_str']
        view_signature = DeviceState.__get_view_signature(view_dict)
        parent_strs = []
        for parent_id in self.get_all_ancestors(view_dict):
            parent_strs.append(DeviceState.__get_view_signature(self.views[parent_id]))
        parent_strs.reverse()
        child_strs = []
        for child_id in self.get_all_children(view_dict):
            child_strs.append(DeviceState.__get_view_signature(self.views[child_id]))
        child_strs.sort()
        view_str = "Activity:%s\nSelf:%s\nParents:%s\nChildren:%s" % (
            self.foreground_activity,
            view_signature,
            "//".join(parent_strs),
            "||".join(child_strs),
        )
        import hashlib

        view_str = hashlib.md5(view_str.encode('utf-8')).hexdigest()
        view_dict['view_str'] = view_str
        return view_str

    def __get_view_structure(self, view_dict):
        """
        get the structure of the given view
        :param view_dict: dict, an element of list DeviceState.views
        :return: dict, representing the view structure
        """
        if 'view_structure' in view_dict:
            return view_dict['view_structure']
        width = DeviceState.get_view_width(view_dict)
        height = DeviceState.get_view_height(view_dict)
        class_name = DeviceState.__safe_dict_get(view_dict, 'class', "None")
        children = {}

        root_x = view_dict['bounds'][0][0]
        root_y = view_dict['bounds'][0][1]

        child_view_ids = self.__safe_dict_get(view_dict, 'children')
        if child_view_ids:
            for child_view_id in child_view_ids:
                child_view = self.views[child_view_id]
                child_x = child_view['bounds'][0][0]
                child_y = child_view['bounds'][0][1]
                relative_x, relative_y = child_x - root_x, child_y - root_y
                children[
                    "(%d,%d)" % (relative_x, relative_y)
                ] = self.__get_view_structure(child_view)

        view_structure = {"%s(%d*%d)" % (class_name, width, height): children}
        view_dict['view_structure'] = view_structure
        return view_structure

    @staticmethod
    def __key_if_true(view_dict, key):
        return key if (key in view_dict and view_dict[key]) else ""

    @staticmethod
    def __safe_dict_get(view_dict, key, default=None):
        value = view_dict[key] if key in view_dict else None
        return value if value is not None else default

    @staticmethod
    def get_view_center(view_dict):
        """
        return the center point in a view
        @param view_dict: dict, an element of DeviceState.views
        @return: a pair of int
        """
        bounds = view_dict['bounds']
        return (bounds[0][0] + bounds[1][0]) / 2, (bounds[0][1] + bounds[1][1]) / 2

    @staticmethod
    def get_view_width(view_dict):
        """
        return the width of a view
        @param view_dict: dict, an element of DeviceState.views
        @return: int
        """
        bounds = view_dict['bounds']
        return int(math.fabs(bounds[0][0] - bounds[1][0]))

    @staticmethod
    def get_view_height(view_dict):
        """
        return the height of a view
        @param view_dict: dict, an element of DeviceState.views
        @return: int
        """
        bounds = view_dict['bounds']
        return int(math.fabs(bounds[0][1] - bounds[1][1]))

    def get_all_ancestors(self, view_dict):
        """
        Get temp view ids of the given view's ancestors
        :param view_dict: dict, an element of DeviceState.views
        :return: list of int, each int is an ancestor node id
        """
        result = []
        parent_id = self.__safe_dict_get(view_dict, 'parent', -1)
        if 0 <= parent_id < len(self.views):
            result.append(parent_id)
            result += self.get_all_ancestors(self.views[parent_id])
        return result

    def get_all_children(self, view_dict):
        """
        Get temp view ids of the given view's children
        :param view_dict: dict, an element of DeviceState.views
        :return: set of int, each int is a child node id
        """
        children = self.__safe_dict_get(view_dict, 'children')
        if not children:
            return set()
        children = set(children)
        for child in children:
            children_of_child = self.get_all_children(self.views[child])
            children.union(children_of_child)
        return children

    def get_app_activity_depth(self, app):
        """
        Get the depth of the app's activity in the activity stack
        :param app: App
        :return: the depth of app's activity, -1 for not found
        """
        depth = 0
        for activity_str in self.activity_stack:
            if not activity_str:
                return -1
            if app.package_name in activity_str:
                return depth
            depth += 1
        return -1

    def get_possible_input(self):
        """
        Get a list of possible input events for this state
        :return: list of InputEvent
        """
        if self.possible_events:
            return [] + self.possible_events
        possible_events = []
        enabled_view_ids = []
        touch_exclude_view_ids = set()
        for view_dict in self.views:
            # exclude navigation bar if exists
            if (
                self.__safe_dict_get(view_dict, 'enabled')
                and self.__safe_dict_get(view_dict, 'visible')
                and self.__safe_dict_get(view_dict, 'resource_id')
                not in [
                    'android:id/navigationBarBackground',
                    'android:id/statusBarBackground',
                ] 
                and self.__safe_dict_get(view_dict, "package") != "com.ohos.sceneboard"
            ):
                enabled_view_ids.append(view_dict['temp_id'])

        
        enabled_view_ids.reverse()

        for view_id in enabled_view_ids:
            if self.__safe_dict_get(self.views[view_id], 'clickable') and not (
                '.widget.EditText' in self.__safe_dict_get(self.views[view_id], 'class')
            ):
                
                possible_events.append(TouchEvent(view=self.views[view_id]))
                touch_exclude_view_ids.add(view_id)
                
                touch_exclude_view_ids = touch_exclude_view_ids.union(
                    self.get_all_children(self.views[view_id])
                )
                
                if "org.y20k.transistor" in self.foreground_activity and \
                        self.views[view_id]['resource_id'] == "org.y20k.transistor:id/player_sheet":
                    possible_events.append(ScrollEvent(view=self.views[view_id], direction="UP"))
                if "org.y20k.transistor" in self.foreground_activity and \
                        self.views[view_id]['resource_id'] == "org.y20k.transistor:id/station_card":
                    possible_events.append(ScrollEvent(view=self.views[view_id], direction="RIGHT"))

        for view_id in enabled_view_ids:
            if self.__safe_dict_get(self.views[view_id], 'scrollable'):
                possible_events.append(
                    ScrollEvent(view=self.views[view_id], direction="UP")
                )
                possible_events.append(
                    ScrollEvent(view=self.views[view_id], direction="DOWN")
                )
                possible_events.append(
                    ScrollEvent(view=self.views[view_id], direction="LEFT")
                )
                possible_events.append(
                    ScrollEvent(view=self.views[view_id], direction="RIGHT")
                )

        for view_id in enabled_view_ids:
            if self.__safe_dict_get(self.views[view_id], 'checkable'):
                possible_events.append(TouchEvent(view=self.views[view_id]))
                touch_exclude_view_ids.add(view_id)
                # fix a bug: add union return values
                touch_exclude_view_ids = touch_exclude_view_ids.union(
                    self.get_all_children(self.views[view_id])
                )

        for view_id in enabled_view_ids:
            # add long click event and do not generate the "long click" event for EditText
            if self.__safe_dict_get(self.views[view_id], 'long_clickable') and not self.__safe_dict_get(self.views[view_id], 'class') == 'android.widget.EditText':
                possible_events.append(LongTouchEvent(view=self.views[view_id]))

        for view_id in enabled_view_ids:
            if self.__safe_dict_get(self.views[view_id], 'editable'):
                from hypothesis import strategies as st
                import string
                sample_text = st.text(alphabet=string.printable,min_size=0, max_size=8).example()
                if random.random() < 0.5:
                    sample_text = st.text(alphabet=string.ascii_letters,min_size=0, max_size=8).example()
                possible_events.append(
                    SetTextEvent(view=self.views[view_id], text=sample_text)
                )
                # add search event for editable view that contains search in its resource id
                if  self.__safe_dict_get(self.views[view_id], 'resource_id') is not None and "search" in self.__safe_dict_get(self.views[view_id], 'resource_id'):
                    sample_text = st.text(alphabet=string.printable,min_size=1, max_size=2).example()
                    if random.random() < 0.5:
                        sample_text = st.text(alphabet=string.ascii_letters,min_size=1, max_size=2).example()
                    possible_events.append(
                        SearchEvent()
                    )
                    possible_events.append(
                        SetTextAndSearchEvent(text=sample_text)
                    )

                touch_exclude_view_ids.add(view_id)
                # TODO figure out what event can be sent to editable views
                pass
        #  for those views that (1) have not been handled, and (2) are leaf views, generate touch events
        for view_id in enabled_view_ids:
            if view_id in touch_exclude_view_ids:
                continue
            children = self.__safe_dict_get(self.views[view_id], 'children')
            if children and len(children) > 0:
                continue

            #  fix a possible bug: we still need to check the property
            # before we add them into "possible_events"
            if self.__safe_dict_get(
                self.views[view_id], 'clickable'
            ) or self.__safe_dict_get(self.views[view_id], 'checkable'):
                possible_events.append(TouchEvent(view=self.views[view_id]))

        # For old Android navigation bars
        # possible_events.append(KeyEvent(name="MENU"))

        for view_id in enabled_view_ids:
            if self.__safe_dict_get(self.views[view_id], 'package') == 'com.tencent.mm' and self.__safe_dict_get(self.views[view_id], 'resource_id') == "com.tencent.mm:id/media_container":
                bounds = self.__safe_dict_get(self.views[view_id], 'bounds')
                x0 = bounds[0][0]
                y0 = bounds[0][1]
                x1 = bounds[1][0]
                y1 = bounds[1][1]
                swipe_x = (x0 + x1) / 2.0
                swipe_y0 = y0 + 3.0 * (y1 - y0) / 4.0
                swipe_y1 = y0 + (y1- y0) / 4.0
                possible_events.append(SwipeEvent(start_x=swipe_x, start_y=swipe_y0, end_x=swipe_x, end_y=swipe_y1, duration = 500))
                possible_events.append(SwipeEvent(start_x=swipe_x, start_y=swipe_y1, end_x=swipe_x, end_y=swipe_y0, duration = 500))


        self.possible_events = possible_events
        return [] + possible_events
    

    def get_text_representation(self, merge_buttons=False):
        """
        Get a text representation of current state
        """
        enabled_view_ids = []
        for view_dict in self.views:
            # exclude navigation bar if exists
            if self.__safe_dict_get(view_dict, 'visible') and \
                self.__safe_dict_get(view_dict, 'resource_id') not in \
               ['android:id/navigationBarBackground',
                'android:id/statusBarBackground'] and \
                self.__safe_dict_get(view_dict, "package") != "com.ohos.sceneboard":
                enabled_view_ids.append(view_dict['temp_id'])
        
        text_frame = "<p id=@ text='&' attr=null bounds=null>#</p>"
        btn_frame = "<button id=@ text='&' attr=null bounds=null>#</button>"
        checkbox_frame = "<checkbox id=@ text='&' attr=null bounds=null>#</checkbox>"
        input_frame = "<input id=@ text='&' attr=null bounds=null>#</input>"
        scroll_frame = "<scrollbar id=@ attr=null bounds=null></scrollbar>"

        view_descs = []
        indexed_views = []
        # available_actions = []
        removed_view_ids = []

        for view_id in enabled_view_ids:
            if view_id in removed_view_ids:
                continue
            # print(view_id)
            view = self.views[view_id]
            clickable = self._get_self_ancestors_property(view, 'clickable')
            scrollable = self.__safe_dict_get(view, 'scrollable')
            checkable = self._get_self_ancestors_property(view, 'checkable')
            long_clickable = self._get_self_ancestors_property(view, 'long_clickable')
            editable = self.__safe_dict_get(view, 'editable')
            actionable = clickable or scrollable or checkable or long_clickable or editable
            checked = self.__safe_dict_get(view, 'checked', default=False)
            selected = self.__safe_dict_get(view, 'selected', default=False)
            content_description = self.__safe_dict_get(view, 'content_description', default='')
            view_text = self.__safe_dict_get(view, 'text', default='')
            # TODO: how to process the class?
            # view_class = self.__safe_dict_get(view, 'class').split('.')[-1]
            bounds = self.__safe_dict_get(view, 'bounds')
            view_bounds = f'{bounds[0][0]},{bounds[0][1]},{bounds[1][0]},{bounds[1][1]}'
            if not content_description and not view_text and not scrollable:  # actionable?
                continue

            # text = self._merge_text(view_text, content_description)
            # view_status = ''
            view_local_id = str(len(view_descs))
            if editable:
                view_desc = input_frame.replace('@', view_local_id).replace('#', view_text)
                if content_description:
                    view_desc = view_desc.replace('&', content_description)
                else:
                    view_desc = view_desc.replace(" text='&'", "")
                # available_actions.append(SetTextEvent(view=view, text='HelloWorld'))
            elif checkable:
                view_desc = checkbox_frame.replace('@', view_local_id).replace('#', view_text)
                if content_description:
                    view_desc = view_desc.replace('&', content_description)
                else:
                    view_desc = view_desc.replace(" text='&'", "")
                # available_actions.append(TouchEvent(view=view))
            elif clickable:  # or long_clickable
                if merge_buttons:
                    # below is to merge buttons, led to bugs
                    clickable_ancestor_id = self._get_ancestor_id(view=view, key='clickable')
                    if not clickable_ancestor_id:
                        clickable_ancestor_id = self._get_ancestor_id(view=view, key='checkable')
                    clickable_children_ids = self._extract_all_children(id=clickable_ancestor_id)
                    if view_id not in clickable_children_ids:
                        clickable_children_ids.append(view_id)
                    view_text, content_description = self._merge_text(clickable_children_ids)
                    checked = self._get_children_checked(clickable_children_ids)
                    # end of merging buttons
                view_desc = btn_frame.replace('@', view_local_id).replace('#', view_text)
                if content_description:
                    view_desc = view_desc.replace('&', content_description)
                else:
                    view_desc = view_desc.replace(" text='&'", "")
                # available_actions.append(TouchEvent(view=view))
                if merge_buttons:
                    for clickable_child in clickable_children_ids:
                        if clickable_child in enabled_view_ids and clickable_child != view_id:
                            removed_view_ids.append(clickable_child)
            elif scrollable:
                # print(view_id, 'continued')
                view_desc = scroll_frame.replace('@', view_local_id)
                # available_actions.append(ScrollEvent(view=view, direction='DOWN'))
                # available_actions.append(ScrollEvent(view=view, direction='UP'))
            else:
                view_desc = text_frame.replace('@', view_local_id).replace('#', view_text)
                if content_description:
                    view_desc = view_desc.replace('&', content_description)
                else:
                    view_desc = view_desc.replace(" text='&'", "")
                # available_actions.append(TouchEvent(view=view))

            allowed_actions = ['touch']
            special_attrs = []
            if editable:
                allowed_actions.append('set_text')
            if checkable:
                allowed_actions.extend(['select', 'unselect'])
                allowed_actions.remove('touch')
            if scrollable:
                allowed_actions.extend(['scroll up', 'scroll down'])
                allowed_actions.remove('touch')
            if long_clickable:
                allowed_actions.append('long_touch')
            if checked or selected:
                special_attrs.append('selected')
            view['allowed_actions'] = allowed_actions
            view['special_attrs'] = special_attrs
            view['local_id'] = view_local_id
            if len(special_attrs) > 0:
                special_attrs = ','.join(special_attrs)
                view_desc = view_desc.replace("attr=null", f"attr={special_attrs}")
            else:
                view_desc = view_desc.replace(" attr=null", "")
            view_desc = view_desc.replace("bounds=null", f"bound_box={view_bounds}")
            view_descs.append(view_desc)
            view['desc'] = view_desc.replace(f' id={view_local_id}', '').replace(f' attr={special_attrs}', '')
            indexed_views.append(view)

        # prefix = 'The current state has the following UI elements: \n' #views and corresponding actions, with action id in parentheses:\n '
        state_desc = '\n'.join(view_descs)
        
        activity = self.foreground_activity.split('/')[-1] if self.foreground_activity else None
        
        # print(views_without_id)
        return state_desc, activity, indexed_views

    def _get_self_ancestors_property(self, view, key, default=None):    
        all_views = [view] + [self.views[i] for i in self.get_all_ancestors(view)]
        for v in all_views:
            value = self.__safe_dict_get(v, key)
            if value:
                return value
        return default

    def get_view_by_attribute(self, attribute_dict,random_select=False):
        """
        get the veiw that matches the attribute dict
        :param attribute_dict: the attribute dict

        """
        view_list = self.views
        ui_element = {}
        for attribute_name, attribute_value in attribute_dict.items():
            if attribute_name == "event_type":
                continue
            if attribute_name == "resourceId":
                ui_element["resource_id"] = attribute_value
            elif attribute_name == "description":
                ui_element["content_description"] = attribute_value
            elif attribute_name == "class":
                ui_element["className"] = attribute_value
            elif attribute_name == "text" or attribute_name == "checked" or attribute_name == "selected":
                ui_element[attribute_name] = attribute_value

        view_list = self.get_view_list_by_atrribute(ui_element, view_list)

        if len(view_list) == 0:
            return None

        if random_select:
            return random.choice(view_list)
        return view_list[0]

    def get_view_list_by_atrribute(
        self, ui_element, origin_list=None
    ):
        """
        Get the view list by atrribute_name
        :param attribute_name: the name of the attribute
        :return: the view list that match the attribute
        """

        if origin_list is None:
            origin_list = self.views
        view_list = []
        for view in origin_list:
            flag = True
            for attribute_key, attribute_value in ui_element.items():
                if view[attribute_key] != attribute_value:
                    flag = False
            if flag:
                view_list.append(view)
        if len(view_list) == 0:
            self.logger.info("No view found for %s" % ui_element)
        return view_list

    # 
    def is_view_exist(self, view_dict):
        """
        
        :param view_dict: view dict
        :return: None or view
        """
        for view in self.views:
            if self.__get_view_str(view) == self.__get_view_str(view_dict):
                return view
            
        for view in self.views:
            if DeviceState.__get_view_signature(view) == DeviceState.__get_view_signature(
                view_dict
            ):
                return view
        return None

    def get_state_screen(self): 
        return self.screenshot_path

    def get_view_desc(self, view):
        content_description = self.__safe_dict_get(view, 'content_description', default='')
        view_text = self.__safe_dict_get(view, 'text', default='')
        scrollable = self.__safe_dict_get(view, 'scrollable')
        view_desc = f'view'
        if scrollable:
            view_desc = f'scrollable view'
        if content_description:
            view_desc += f' "{content_description}"'
        if view_text:
            view_text = view_text.replace('\n', '  ')
            view_text = f'{view_text[:20]}...' if len(view_text) > 20 else view_text
            view_desc += f' with text "{view_text}"'
        return view_desc
        
    def get_described_actions(self):
        """
        Get a text description of current state
        """
        enabled_view_ids = []
        for view_dict in self.views:
            # exclude navigation bar if exists
            if self.__safe_dict_get(view_dict, 'visible') and \
                self.__safe_dict_get(view_dict, 'resource_id') not in \
               ['android:id/navigationBarBackground',
                'android:id/statusBarBackground']:
                enabled_view_ids.append(view_dict['temp_id'])

        view_descs = []
        available_actions = []
        for view_id in enabled_view_ids:
            view = self.views[view_id]
            clickable = self._get_self_ancestors_property(view, 'clickable')
            scrollable = self.__safe_dict_get(view, 'scrollable')
            checkable = self._get_self_ancestors_property(view, 'checkable')
            long_clickable = self._get_self_ancestors_property(view, 'long_clickable')
            editable = self.__safe_dict_get(view, 'editable')
            actionable = clickable or scrollable or checkable or long_clickable or editable
            checked = self.__safe_dict_get(view, 'checked')
            selected = self.__safe_dict_get(view, 'selected')
            content_description = self.__safe_dict_get(view, 'content_description', default='')
            view_text = self.__safe_dict_get(view, 'text', default='')
            if not content_description and not view_text and not scrollable:  # actionable?
                continue
            
            view_status = ''
            if editable:
                view_status += 'editable '
            if checked or selected:
                view_status += 'checked '
            view_desc = f'- a {view_status}view'
            if content_description:
                content_description = content_description.replace('\n', '  ')
                content_description = f'{content_description[:20]}...' if len(content_description) > 20 else content_description
                view_desc += f' "{content_description}"'
            if view_text:
                view_text = view_text.replace('\n', '  ')
                view_text = f'{view_text[:20]}...' if len(view_text) > 20 else view_text
                view_desc += f' with text "{view_text}"'
            if actionable:
                view_actions = []
                if editable:
                    view_actions.append(f'edit ({len(available_actions)})')
                    available_actions.append(SetTextEvent(view=view, text='HelloWorld'))
                if clickable or checkable:
                    view_actions.append(f'click ({len(available_actions)})')
                    available_actions.append(TouchEvent(view=view))
                # if checkable:
                #     view_actions.append(f'check/uncheck ({len(available_actions)})')
                #     available_actions.append(TouchEvent(view=view))
                # if long_clickable:
                #     view_actions.append(f'long click ({len(available_actions)})')
                #     available_actions.append(LongTouchEvent(view=view))
                if scrollable:
                    view_actions.append(f'scroll up ({len(available_actions)})')
                    available_actions.append(ScrollEvent(view=view, direction='UP'))
                    view_actions.append(f'scroll down ({len(available_actions)})')
                    available_actions.append(ScrollEvent(view=view, direction='DOWN'))
                view_actions_str = ', '.join(view_actions)
                view_desc += f' that can {view_actions_str}'
            view_descs.append(view_desc)
        view_descs.append(f'- a key to go back ({len(available_actions)})')
        available_actions.append(KeyEvent(name='BACK'))
        state_desc = 'The current state has the following UI views and corresponding actions, with action id in parentheses:\n '
        state_desc += ';\n '.join(view_descs)
        return state_desc, available_actions

    def get_action_desc(self, action):
        desc = action.event_type
        if isinstance(action, KeyEvent):
            desc = f'- go {action.name.lower()}'
        if isinstance(action, UIEvent):
            action_name = action.event_type
            if isinstance(action, LongTouchEvent):
                action_name = 'long click'
            elif isinstance(action, SetTextEvent):
                action_name = f'enter "{action.text}" into'
            elif isinstance(action, ScrollEvent):
                action_name = f'scroll {action.direction.lower()}'
            desc = f'- {action_name} {self.get_view_desc(action.view)}'
        return desc