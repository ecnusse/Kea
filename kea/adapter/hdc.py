# This is the interface for hdc
import datetime
import json
from typing import Dict
import subprocess
import logging
import re
from .adapter import Adapter
import time
import os
import pathlib
import typing
import time
from ..utils import get_yml_config

try:
    from hmdriver2.driver import Driver, HmClient
except ImportError:
    pass

try:
    from shlex import quote # Python 3
except ImportError:
    from pipes import quote # Python 2
from abc import abstractmethod, ABC


config_dir = get_yml_config()

if config_dir["env"].lower() in ["mac", "macos", "linux", "unix"]:
    SYSTEM = "Linux"
elif config_dir["env"].lower() in ["win", "windows"]:
    SYSTEM = "windows"
else:
    raise f"No support for system {config_dir['env']}"

if SYSTEM == "windows":
    HDC_EXEC = "hdc.exe"
elif SYSTEM == "Linux":
    HDC_EXEC = "hdc"


class HDCException(Exception):
    """
    Exception in HDC connection
    """
    pass

class HierarchyDumpError(HDCException):
    """
    Error during dumping hierarchy
    """

class Dumper(ABC):

    @abstractmethod
    def preprocess_views(self):
        pass

class HDC(Adapter):
    """
    interface of HDC
    """
    global HDC_EXEC
    # * HDC command for device info. See the doc below.
    # * https://github.com/codematrixer/awesome-hdc?tab=readme-ov-file#%E6%9F%A5%E7%9C%8B%E8%AE%BE%E5%A4%87%E4%BF%A1%E6%81%AF
    UP = 0
    DOWN = 1
    DOWN_AND_UP = 2
    MODEL_PROPERTY = "const.product.model"
    DEVICE_PROPERTY = "const.product.name"
    VERSION_OS_PROPERTY = "const.product.software.version"
    CPU_STRUCTER_PROPERTY = "const.product.cpu.abilist"
    # VERSION_SDK_PROPERTY = ''
    # VERSION_RELEASE_PROPERTY = ''

    def __init__(self, device=None, hmclient=None):
        """
        initiate a HDC connection from serial no
        the serial no should be in output of `hdc devices`
        :param device: instance of Device
        :return:
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.hmclient: Driver = hmclient
        self.device = device

        self.cmd_prefix = [HDC_EXEC, "-t", device.serial]

    
    def set_up(self):
        self.logger.info(f"[CONNECTION] Setting up Adapter hdc.")
        # make the temp path in output dir to store the dumped layout result
        temp_path = os.path.join(
            os.getcwd(), self.device.output_dir, "temp"
        )
        if os.path.exists(temp_path):
            import shutil
            shutil.rmtree(temp_path)
        os.mkdir(temp_path)

    def tear_down(self):
        pass
        # temp_path = os.getcwd() + "/" + self.device.output_dir + "/temp"
        # if os.path.exists(temp_path):
        #     import shutil
        #     shutil.rmtree(temp_path)

    
    def run_cmd(self, extra_args):
        """
        run a hdc command and return the output
        :return: output of hdc command
        @param extra_args: arguments to run in hdc
        """
        if isinstance(extra_args, str):
            extra_args = extra_args.split()
        if not isinstance(extra_args, list):
            msg = "invalid arguments: %s\nshould be list or str, %s given" % (extra_args, type(extra_args))
            self.logger.warning(msg)
            raise HDCException(msg)

        # args = [HDC_EXEC]
        args = [] + self.cmd_prefix
        args += extra_args

        self.logger.debug('Runing command:')
        self.logger.debug(" ".join([str(arg) for arg in args]))
        r = subprocess.check_output(args).strip()
        if not isinstance(r, str):
            r = r.decode()
        self.logger.debug('Return value:')
        self.logger.debug(r)
        return r

    
    def shell(self, extra_args):
        """
        run an `hdc shell` command
        @param extra_args:
        @return: output of hdc shell command
        """

        

        if isinstance(extra_args, str):
            extra_args = extra_args.split()
        if not isinstance(extra_args, list):
            msg = "invalid arguments: %s\nshould be list or str, %s given" % (extra_args, type(extra_args))
            self.logger.warning(msg)
            raise HDCException(msg)

        shell_extra_args = ['shell'] + [ quote(arg) for arg in extra_args ]

        try:
            return self.run_cmd(shell_extra_args)
        except FileNotFoundError as e:
            raise HDCException(f"""{HDC_EXEC} command not found. You're running HMDroidbot in {SYSTEM} mode. Please checkout the SYSTEM variable or your envirnment""")

    def check_connectivity(self):
        """
        check if hdc is connected
        :return: True for connected
        """
        #TODO not support this method
        r = self.run_cmd("list targets")
        return not r.startswith("[Empty]")

    def connect(self):
        """
        connect hdc
        """
        self.logger.debug("connected")

    def disconnect(self):
        """
        disconnect hdc
        """
        self.logger.info("[CONNECTION] %s is disconnected" % self.__class__.__name__)

    def get_property(self, property_name):
        """
        get the value of property
        @param property_name:
        @return:
        """
        return self.shell(["param", "get", property_name])

    def get_model_number(self):
        """
        Get device model number. e.g. SM-G935F
        """
        return self.get_property(HDC.MODEL_PROPERTY)

    def get_sdk_version(self):
        """
        Get version of SDK
        """
        raise NotImplementedError
        return int(self.get_property(HDC.VERSION_SDK_PROPERTY))
    
    def get_device_name(self):
        """
        Get the device Name
        """
        return self.get_property(HDC.DEVICE_PROPERTY)

    def get_release_version(self):
        """
        Get release version, e.g. 4.3, 6.0
        """
        raise NotImplementedError
        return self.get_property(HDC.VERSION_RELEASE_PROPERTY)

    def get_installed_apps(self):
        """
        Get the package names and apk paths of installed apps on the device
        :return: a dict, each key is a package name of an app and each value is the file path to the apk
        """
        app_lines = self.shell("bm dump -a").splitlines()
        installed_bundle = []
        for app_line in app_lines:
            installed_bundle.append(app_line.strip())
        return installed_bundle

    def get_display_density(self):
        display_info = self.get_display_info()
        if 'density' in display_info:
            return display_info['density']
        else:
            return -1.0

    def __transform_point_by_orientation(self, xy, orientation_orig, orientation_dest):
        (x, y) = xy
        if orientation_orig != orientation_dest:
            if orientation_dest == 1:
                _x = x
                x = self.get_display_info()['width'] - y
                y = _x
            elif orientation_dest == 3:
                _x = x
                x = y
                y = self.get_display_info()['height'] - _x
        return x, y

    def get_orientation(self):
        """
        ## ! Function not implemented
        #### TODO hdc rotate cmd not found 
        """
        import inspect
        self.logger.debug(f"function:get_orientation not implemented. Called by {inspect.stack()[1].function}")
        return 1

    def unlock(self):
        """
        Unlock the screen of the device
        """
        self.shell("uitest uiInput keyEvent Home")
        self.shell("uitest uiInput keyEvent Back")

    def press(self, key_code):
        """
        Press a key
        """
        key_code = "Back" if key_code.lower() == "back" else key_code
        key_code = "Home" if key_code.lower() == "home" else key_code
        self.shell("uitest uiInput keyEvent %s" % key_code)

    def touch(self, x, y, orientation=-1, event_type=DOWN_AND_UP):
        if orientation == -1:
            orientation = self.get_orientation()
        self.shell("uitest uiInput click %d %d" %
                   self.__transform_point_by_orientation((x, y), orientation, self.get_orientation()))

    def long_touch(self, x, y, orientation=-1):
        """
        Long touches at (x, y)
        """
        if orientation == -1:
            orientation = self.get_orientation()
        self.shell("uitest uiInput longClick %d %d" %
                   self.__transform_point_by_orientation((x, y), orientation, self.get_orientation()))

    def drag(self, start_xy, end_xy, duration, orientation=-1):
        """
        Sends drag event n PX (actually it's using C{input swipe} command.
        @param start_xy: starting point in pixel
        @param end_xy: ending point in pixel
        @param duration: duration of the event in ms
        @param orientation: the orientation (-1: undefined)
        """
        (x0, y0) = start_xy
        (x1, y1) = end_xy
        if orientation == -1:
            orientation = self.get_orientation()
        (x0, y0) = self.__transform_point_by_orientation((x0, y0), orientation, self.get_orientation())
        (x1, y1) = self.__transform_point_by_orientation((x1, y1), orientation, self.get_orientation())

        speed = 2000
        self.shell("uitest uiInput swipe %d %d %d %d %d" % (x0, y0, x1, y1, speed))
        
    def type(self, text):
        # hdc shell uitest uiInput inputText 100 100 hello
        if isinstance(text, str):
            escaped = text.replace("%s", "\\%s")
            encoded = escaped.replace(" ", "%s")
        else:
            encoded = str(text)
        # TODO find out which characters can be dangerous, and handle non-English characters
        self.shell("input text %s" % encoded)

    """
    The following function is especially for HarmonyOS NEXT
    """
    @staticmethod
    def safe_dict_get(view_dict, key, default=None):
        value = view_dict[key] if key in view_dict else None
        return value if value is not None else default
    
    @staticmethod
    def get_relative_path(absolute_path:str) -> str:
        """
        return the relative path in win style
        """
        workspace = pathlib.Path(os.getcwd())
        try:
            if SYSTEM == "windows":
                relative_path = pathlib.PureWindowsPath(pathlib.Path(absolute_path).relative_to(workspace))
                return relative_path
            elif SYSTEM == "Linux":
                return pathlib.Path(absolute_path).relative_to(workspace)
        except ValueError:
            # When app path is not the subpath of workspace, return itself.
            return absolute_path
    
    def push_file(self, local_file, remote_dir="/sdcard/"):
        """
        push file/directory to target_dir
        :param local_file: path to file/directory in host machine
        :param remote_dir: path to target directory in device
        :return:
        """
        if not os.path.exists(local_file):
            self.logger.warning("push_file file does not exist: %s" % local_file)
        self.run_cmd(["file send", local_file, remote_dir])

    def pull_file(self, remote_file, local_file):
        r = self.run_cmd(["file", "recv", remote_file, local_file])
        assert not r.startswith("[Fail]"), "Error with receiving file"
        
    def get_views(self, output_dir):

        #* Use hidumper to get views
        # dumper = HiDumper(hdc=self)
        # views = dumper.hierachy

        #* use uitest dumper to get views
        # dumper = UitestDumper(hdc=self, output_dir=output_dir)
        # views = dumper.get_views()

        
        #* use HMClient dumper to get views
        if HmDriverDumper.device is None:
            HmDriverDumper.device = self.hmclient._client
        dumper = HmDriverDumper(hdc=self)
        views = dumper.get_views()

        return views

class HiDumper(Dumper):

    def print_time_cost(self, info):
        current_time = time.perf_counter()
        print(f"{info} cost time {current_time - self.cached_time:4f}s")
        self.cached_time = current_time

    def __init__(self, hdc:HDC):

        """
        process the stdout to get the raw hierachy
        """
        self.indent_cache = -1
        self.windowInfo = dict()
        self._hierachy:list[dict] = list()

        self.hdc = hdc
        focus_window = self.get_focus_window()
        self.cached_time = time.perf_counter()

        temp_path = os.path.join(hdc.device.output_dir, "temp.txt")
        
        with open(temp_path, "w") as fp:
            cmd = f"{HDC_EXEC} -t {self.hdc.device.serial} shell hidumper -s WindowManagerService -a '-w {focus_window} -inspector'"
            subprocess.run(cmd.split(), stdout=fp, stderr=subprocess.PIPE, text=True)  

        # print(f"txt size is {os.path.getsize('temp.txt')}")
        # self.print_time_cost("hidumper to txt")

        with open(temp_path, "r") as fp:
            self.dump_layout(fp)

        # self.print_time_cost("read txt")

        self.adapt_hierachy()

        # self.print_time_cost("adapt hierachy")

    def dump_target_window_to_file(self, focus_window, fp:typing.IO):
        cmd = [HDC_EXEC, "-t", self.hdc.device.serial, "shell", "hidumper", "-s", "WindowManagerService", "-a", f"'-w {focus_window} -inspector'"]
        subprocess.run(cmd, stdout=fp, stderr=subprocess.STDOUT)

    def get_focus_window(self):
        r = self.hdc.run_cmd(f"{HDC_EXEC} -t {self.hdc.device.serial} shell hidumper -s WindowManagerService -a '-a'")

        match = re.search(r'Focus window:\s*(\d+)', r)

        if match:
            focus_window = match.group(1)
            return focus_window
        else:
            raise HDCException("Error when getting focus_window")
    
    def preprocess_views(self):
        return self.hierachy

    def get_indent(self, line):
        return int((len(line) - len(line.lstrip())) / 2)
    
    def get_line_info(self, line:str):
        # print(f"getting_line: {line}")
        return [ _.strip(" |\n") for _ in line.split(":", maxsplit=1)]
    
    def get_window_info(self, line:str, fp:typing.Iterable[str]):
        while "last vsyncId" not in line:
            key, value = self.get_line_info(line)
            self.windowInfo[key] = value
            line = next(fp)
    
    def get_hierachy(self, line:str, fp:typing.Iterable[str]):
        if not line.strip():
            raise StopIteration
        
        node_indent = self.get_indent(line)
        
        node = {"type":line.split()[1],
                "child_count":int(line.split(":")[-1]),
                "level": node_indent}
        
        line = next(fp)
        while "->" not in line and line.strip():
            # print(line)
            key, value = self.get_line_info(line)
            node[key] = value
            line = next(fp)

        node["children"] = []
        self._hierachy.append(node)

        if node_indent > 1:
            for parent in reversed(self._hierachy):
                if parent["level"] == node_indent - 1:
                    # print(node)
                    parent["children"].append(node["ID"])
                    break
        return line


    def dump_layout(self, fp):

        # the parsing procedure can be reconized as a state machine
        # we should first skip the irrelavent hinting info, then parse the window info, finally the hierachy tree
        # skip hinting ====begin_flag===> parse window info ====widget_flag===> parse hierachy tree 
        begin_flag = False
        widget_flag = False

        while True:
            try:
                if not widget_flag:
                    line = next(fp)

                if "WindowManagerService" in line:
                    begin_flag = True
                    continue
                
                if not begin_flag:
                    continue

                if "->" in line:
                    widget_flag = True
                
                if not widget_flag:
                    self.get_window_info(line, fp)
                else:
                    line = self.get_hierachy(line, fp)

            except StopIteration:
                # End of file
                break
        
        # print(f"_hierachy size is {len(self._hierachy)}")

        # if logger.level != logging.DEBUG:
        #     return
        # # the following code is for assertion
        # for node in self._hierachy:
        #     assert node["child_count"] == len(node["children"]), node

    """
    proccess the hierachy to adapt it to droidbot style
    """

    def adapt_hierachy(self):
        self.hierachy = []
        uiextension_children = []
        id_map = dict()

        for i, _node in enumerate(self._hierachy):
            node = dict()
            if _node["type"] == "UIExtensionComponent" or _node["ID"] in uiextension_children:
                uiextension_children.extend(_node["children"])
                continue
            for key, value in _node.items():
                if key in ["visible", "clickable", "checkable", "scrollable", "checked"]:
                    node[key] = bool(int(value))
                    continue
                if key == "longClickable":
                    node["long_clickable"] = bool(int(value))
                    continue
                if key == "ID":
                    node["accessibilityId"] = (old_id := int(value))
                    node["temp_id"] = i
                    id_map[old_id] = i
                    continue
                if key == "children":
                    node[key] = [int(_) for _ in value]
                    continue
                if key == "type":
                    node["class"] = value
            
            # proccess the bounds
            top, left, width, height = [int(float(_node["top"])), int(float(_node["left"])),
                                        int(float(_node["width"])), int(float(_node["height"]))]
            node["bounds"] = [[left, top], [left+width, top+height]]
            node["size"] = f"{width}*{height}"

            #! TODO hidumper抓下来的控件没有enabled信息，这里先默认为True，日后若接口改变需更改
            node["enabled"] = True

            self.hierachy.append(node)
        
        for _node in self.hierachy:
            for old_id, new_id in id_map.items():
                if old_id in _node["children"]:
                    _node["children"].remove(old_id)
                    _node["children"].append(new_id)
        
        self.hierachy

class UitestDumper(Dumper):
    """
    This class use uitest to dump layout. Which is 25 times slower than Hidumper.
    But uitest dumpLayout can get some useful messages such as key and pagePath.

    core cmd: hdc shell uitest dumpLayout
    """

    _views = None

    def __init__(self, hdc:HDC, output_dir:str):
        self.output_dir = output_dir
        self.hdc = hdc

    def dump_view(self)->str:
        """
        Using uitest to dumpLayout, and return the remote path of the layout file
        :Return: remote path
        """
        r = self.hdc.shell("uitest dumpLayout")
        assert "DumpLayout saved to" in r, "Error when dumping layout"

        remote_path = r.split(":")[-1]
        return remote_path

    def preprocess_views(self, views_path):
        """
        bfs the view tree and turn it into the android style
        views list
        ### :param: view path
        """
        from collections import deque
        self._views = []

        with open(views_path, "r", encoding="utf-8") as f:
            import json
            self.views_raw = json.load(f)

        # process the root node
        self.views_raw["attributes"]["parent"] = -1

        # add it into a queue to bfs
        queue = deque([self.views_raw])
        temp_id = 0

        while queue:
            node: Dict = queue.popleft()

            # process the node and add the hierachy info so that Droidbot can
            # recongnize while traversing
            node["attributes"]["temp_id"] = temp_id
            node["attributes"]["child_count"] = len(node["children"])
            node["attributes"]["children"] = list()

            # process the view, turn it into android style and add to view list
            self._views.append(self.get_adb_view(node["attributes"]))

            # bfs the tree
            for child in node["children"]:
                child["attributes"]["parent"] = temp_id
                if "bundleName" in node["attributes"]:
                    child["attributes"]["bundleName"] = HDC.safe_dict_get(node["attributes"], "bundleName")
                    assert self.hdc.safe_dict_get(node["attributes"], "pagePath") is not None, "pagePath not exist"
                    child["attributes"]["pagePath"] = self.hdc.safe_dict_get(node["attributes"], "pagePath")
                queue.append(child)

            temp_id += 1

        # get the 'children' attributes
        self.get_view_children()

        return self._views

    def get_view_children(self):
        """
        get the 'children' attributes by the 'parent'
        """
        for view in self._views:
            temp_id = HDC.safe_dict_get(view, "parent")
            if temp_id > -1:
                self._views[temp_id]["children"].append(view["temp_id"])
                assert self._views[temp_id]["temp_id"] == temp_id

    def get_adb_view(self, raw_view:dict):
        """
        process the view and turn it into the android style
        """
        view = dict()
        for key, value in raw_view.items():
            # adapt the attributes into adb form
            if key in ["visible", "checkable", "enabled", "clickable", \
                       "scrollable", "selected", "focused", "checked"]:
                view[key] = True if value in ["True", "true"] else False
                continue
            if key == "longClickable":
                view["long_clickable"] = bool(value.lower() == "true")
                continue
            if key == "bounds":
                view[key] = self.get_bounds(value)
                view["size"] = self.get_size(value)
                continue
            if key == "bundleName":
                view["package"] = value
                continue
            if key == "description":
                view["content_description"] = value
                continue
            if key == "type":
                view["class"] = value
                continue
            if key == "key":
                view["resource_id"] = value
                continue
            view[key] = value

        if view["class"] in {"RichEditor", "TextInput", "TextArea"}:
            view["editable"] = True

        return view

    def get_bounds(self, raw_bounds:str):
        # capturing the coordinate of the bounds and return 2-dimensional list
        # e.g.  "[10,20][30,40]" -->  [[10, 20], [30, 40]]
        import re
        size_pattern = r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]"
        match = re.search(size_pattern, raw_bounds)
        if match:
            return [[int(match.group(1)), int(match.group(2))], \
                    [int(match.group(3)), int(match.group(4))]]

    def get_size(self, raw_bounds:str):
        bounds = self.get_bounds(raw_bounds)
        return f"{bounds[1][0]-bounds[0][0]}*{bounds[1][1]-bounds[0][1]}"

    @property
    def views(self):
        if self._views is None:
            if self.output_dir is None:
                return None

            remote_path = self.dump_view()

            file_name = os.path.basename(remote_path)
            temp_path = os.path.join(self.output_dir, "temp")
            local_path = os.path.join(os.getcwd(), temp_path, file_name)

            self.hdc.pull_file(remote_path, HDC.get_relative_path(local_path))

            return self.preprocess_views(local_path)

    def get_views(self):
        return self.views


class HmDriverDumper(Dumper):
    """
    This class use HMDriver and uitest to dump layout.
    """

    device: "HmClient" = None

    def __init__(self, hdc: HDC):
        self.hdc = hdc

    def dump_view(self) -> str:
        """
        Using uitest to dumpLayout, and return the remote path of the layout file
        :Return: remote path
        """

        r = self._request_hierarchy()
        if r is None:
            raise HierarchyDumpError("error when dumping hierarchy")
        return r

    def _request_hierarchy(self):
        request_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        params = {"api": "captureLayout", "args": []}

        msg = {
            "module": "com.ohos.devicetest.hypiumApiHelper",
            "method": "Captures",
            "params": params,
            "request_id": request_id,
        }

        self.device._send_msg(msg)
        buffer_size = 1024 * 16
        full_msg = bytearray()
        r = None
        while True:
            try:
                relay = self.device.sock.recv(buffer_size)
                full_msg.extend(relay)
                r = json.loads(full_msg)
                break
            except json.JSONDecodeError as NOT_EOF:
                buffer_size *= 4
                continue
            except (TimeoutError, UnicodeDecodeError) as e:
                break

        return r["result"] if r is not None else None

    def preprocess_views(self, views_dict):
        """
        bfs the view tree and turn it into the android style
        views list
        ### :param: view path
        """
        from collections import deque

        self._views = []

        self.views_raw = views_dict

        # process the root node
        self.views_raw["attributes"]["parent"] = -1

        # add it into a queue to bfs
        queue = deque([self.views_raw])
        temp_id = 0

        while queue:
            node: dict = queue.popleft()

            # process the node and add the hierachy info so that Droidbot can
            # recongnize while traversing
            node["attributes"]["temp_id"] = temp_id
            node["attributes"]["child_count"] = len(node["children"])
            node["attributes"]["children"] = list()

            # process the view, turn it into android style and add to view list
            self._views.append(self.get_adb_view(node["attributes"]))

            # bfs the tree
            for child in node["children"]:
                child["attributes"]["parent"] = temp_id
                if "bundleName" in node["attributes"]:
                    child["attributes"]["bundleName"] = HDC.safe_dict_get(
                        node["attributes"], "bundleName"
                    )
                    assert (
                        self.hdc.safe_dict_get(node["attributes"], "pagePath")
                        is not None
                    ), "pagePath not exist"
                    child["attributes"]["pagePath"] = self.hdc.safe_dict_get(
                        node["attributes"], "pagePath"
                    )
                queue.append(child)

            temp_id += 1

        # get the 'children' attributes
        self.get_view_children()

        return self._views

    def get_view_children(self):
        """
        get the 'children' attributes by the 'parent'
        """
        for view in self._views:
            temp_id = HDC.safe_dict_get(view, "parent")
            if temp_id > -1:
                self._views[temp_id]["children"].append(view["temp_id"])
                assert self._views[temp_id]["temp_id"] == temp_id

    def get_adb_view(self, raw_view: dict):
        """
        process the view and turn it into the android style
        """
        view = dict()
        for key, value in raw_view.items():
            # adapt the attributes into adb form
            if key in [
                "visible",
                "checkable",
                "enabled",
                "clickable",
                "scrollable",
                "selected",
                "focused",
                "checked",
            ]:
                view[key] = True if value in ["True", "true"] else False
                continue
            if key == "longClickable":
                view["long_clickable"] = bool(value.lower()=="true")
                continue
            if key == "bounds":
                view[key] = self.get_bounds(value)
                view["size"] = self.get_size(value)
                continue
            if key == "bundleName":
                view["package"] = value
                continue
            if key == "description":
                view["content_description"] = value
                continue
            if key == "type":
                view["class"] = value
                continue
            if key == "key":
                view["resource_id"] = value
                continue
            view[key] = value

        if view["class"] in {"RichEditor", "TextInput", "TextArea"}:
            view["editable"] = True

        return view

    def get_bounds(self, raw_bounds: str):
        # capturing the coordinate of the bounds and return 2-dimensional list
        # e.g.  "[10,20][30,40]" -->  [[10, 20], [30, 40]]
        import re

        size_pattern = r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]"
        match = re.search(size_pattern, raw_bounds)
        if match:
            return [
                [int(match.group(1)), int(match.group(2))],
                [int(match.group(3)), int(match.group(4))],
            ]

    def get_size(self, raw_bounds: str):
        bounds = self.get_bounds(raw_bounds)
        return f"{bounds[1][0]-bounds[0][0]}*{bounds[1][1]-bounds[0][1]}"

    @property
    def views(self):
        view_dict = self.dump_view()
        return self.preprocess_views(view_dict)

    def get_views(self):
        return self.views
