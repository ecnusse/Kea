from typing import List, Dict
import uiautomator2
import xml.etree.ElementTree as ET
import rtree
from ..utils import deprecated

class Uiautomator2_Helper:
    def __init__(self, device=None, package_name = None):
        if device is None:
            from kea.device import Device

            device = Device()
        self.device: Device = device

        self.u2: uiautomator2.Device = device.u2
        # self.u2 = uiautomator2.connect("emulator-5554")
        self.ignore_ad: bool = device.ignore_ad
        if self.ignore_ad:
            import re

            self.__first_cap_re = re.compile("(.)([A-Z][a-z]+)")
            self.__all_cap_re = re.compile("([a-z0-9])([A-Z])")

        self.package_name: str = package_name

    def __id_convert(self, name):
        name = name.replace(".", "_").replace(":", "_").replace("/", "_")
        s1 = self.__first_cap_re.sub(r"\1_\2", name)
        return self.__all_cap_re.sub(r"\1_\2", s1).lower()

    def __view_tree_to_list(self, view_tree, view_list: List):
        tree_id = len(view_list)
        view_tree['temp_id'] = tree_id

        bounds = [[-1, -1], [-1, -1]]
        bounds[0][0] = view_tree['bounds'][0]
        bounds[0][1] = view_tree['bounds'][1]
        bounds[1][0] = view_tree['bounds'][2]
        bounds[1][1] = view_tree['bounds'][3]
        width = bounds[1][0] - bounds[0][0]
        height = bounds[1][1] - bounds[0][1]
        view_tree['size'] = "%d*%d" % (width, height)
        view_tree['bounds'] = bounds

        view_list.append(view_tree)
        children_ids = []
        for child_tree in view_tree['children']:
            if self.ignore_ad and child_tree['resource_id'] is not None:
                id_word_list = self.__id_convert(child_tree['resource_id']).split('_')
                if "ad" in id_word_list or "banner" in id_word_list:
                    continue
            child_tree['parent'] = tree_id
            self.__view_tree_to_list(child_tree, view_list)
            children_ids.append(child_tree['temp_id'])
        view_tree['children'] = children_ids

    def xml_to_dict(self, element) -> Dict:
        # Initialize the result dictionary
        result = {}

        # Process attributes
        attributes = {
            "package": element.get("package"),
            "visible": element.get("visible-to-user") == "true",
            "checkable": element.get("checkable") == "true",
            "child_count": len(element),
            "editable": element.get("class") == "android.widget.EditText",
            "clickable": element.get("clickable") == "true",
            "is_password": element.get("password") == "true",
            "focusable": element.get("focusable") == "true",
            "enabled": element.get("enabled") == "true",
            "drawing-order": int(element.get("drawing-order")) if element.get("drawing-order") else None,
            "content_description": element.get("content-desc")
            if element.get("content-desc")
            else None,
        }

        result = attributes

        # Recursively process children
        for child in element:
            child_data = self.xml_to_dict(child)
            if "children" in result:
                result["children"].append(child_data)
            else:
                result["children"] = [child_data]
        if len(element) == 0:
            result["children"] = []
        result["focused"] = element.get("focused") == "true"

        # Remove the square brackets and split the string by commas
        split_values = (
            element.get("bounds")
            .replace("][", ",")
            .replace("]", "")
            .replace("[", "")
            .split(",")
        )
        # Convert the substrings to integers and create a list
        integer_list = [int(value) for value in split_values]

        result["bounds"] = integer_list

        result["resource_id"] = (
            element.get("resource-id") if element.get("resource-id") else None
        )
        result["checked"] = element.get("checked") == "true"
        result["text"] = element.get("text") if element.get("text") else None
        result["class"] = element.get("class")
        result["scrollable"] = element.get("scrollable") == "true"
        result["selected"] = element.get("selected") == "true"
        result["long_clickable"] = element.get("long-clickable") == "true"

        return result

    def select_target_root_node(self, xml):
        """
        select a target root node from the view tree
        因为uiautomator dump出来的xml file中有可能存在多个root node,我们需要选择我们关心的root node
        :param xml: the xml
        :return: the selected root node
        """
        # exclude some package
        exlude_package = ["com.android.systemui","com.github.uiautomator"]
        # iterate all the root nodes from the xml node, and select the one we want
        root = ET.fromstring(xml)
        packages = {child.get("package") : child for child in root if child.tag == "node"}
        if self.package_name in packages:
            return packages[self.package_name]
        else:
            for package in packages:
                if package in exlude_package:
                    continue
                return packages[package]
        return None

    def dump_view(self) -> Dict:
        """
        dump the current view
        :return: the view tree
        """
        # get the xml file of the current view
        xml = self.u2.dump_hierarchy()
        # select the target root node from the xml file
        view_tree = self.select_target_root_node(xml)
        # convert the xml file to dict
        view_tree = self.xml_to_dict(view_tree)
        
        # Try to prune a sub-tree according to the drawing-order, deprecated.
        # self.prune_blocked_views(view_tree)
        
        DrawingOrderSetter(view_tree)

        return view_tree
    
    @deprecated("The pruning algorithm is not able to calulate the cover relations")
    def prune_blocked_views(self, view_tree):
        """
        Try to prune a sub-tree according to the drawing-order
        """
        width = len(view_tree["children"])
        if width == 0:
            return
        if width >= 2:
            bounds_lt = [child["bounds"] for child in view_tree["children"]]
            if self.bounds_intersect(bounds_lt):
                drawing_orders = [child["drawing-order"] for child in view_tree["children"]]
                
                # get subtree drew on top
                top_subtree = view_tree["children"][drawing_orders.index(width)]
                
                # Exlude the statusBar and navigationBar
                if top_subtree["resource_id"] in \
                    ['android:id/navigationBarBackground',
                     'android:id/statusBarBackground']:
                    pass
                else:
                    view_tree["children"] = [top_subtree]
                           
        for child in view_tree["children"]:
            self.prune_blocked_views(child)

    @deprecated("The pruning algorithm is not able to calulate the cover relations")
    def bounds_intersect(self, bounds_lt):
        
        def intersects(bounds_A, bounds_B):
            vertexs = [[bounds_A[0], bounds_A[1]],
                       [bounds_A[0], bounds_A[3]],
                       [bounds_A[2], bounds_A[1]],
                       [bounds_A[2], bounds_A[3]]]
            
            x1_B, y1_B, x2_B, y2_B = bounds_B
            
            for x, y in vertexs:
                if x1_B < x < x2_B and y1_B < y < y2_B:
                    return False
            
            return True
                     
        for i in range(len(bounds_lt)):
            for j in range(i + 1, len(bounds_lt)):
                if intersects(bounds_lt[i], bounds_lt[j]):
                    return True
        return False       

    def get_views(self) -> List:
        """
        get the view list of the current state
        :return: the view list
        """
        view_tree = self.dump_view()
        if not view_tree:
            return None
        view_tree['parent'] = -1
        view_list = []
        self.__view_tree_to_list(view_tree, view_list)
        return view_list


class DrawingOrderSetter:
    def __init__(self, view_tree):
        self.global_drawing_order = 0
        self.views = []
        self.resolution = view_tree["bounds"]
        self.idx = rtree.index.Index()
        self.set_drawing_orders(view_tree)
   
    def set_drawing_orders(self, view_tree):
        view_tree["global_drawing_order"] = self.global_drawing_order
        view_tree["covered"] = False
        self.views.append(view_tree)

        # if current widget is clickable
        if view_tree["clickable"]:
            # delete all the clickable widgets covered by this widget
            if (covered_widget_ids := list(self.idx.contains(view_tree["bounds"]))):
                for covered_widget_id in covered_widget_ids:
                    self.views[covered_widget_id]["covered"] = True
                    self.idx.delete(covered_widget_id,
                                    self.views[covered_widget_id]["bounds"])

            # add the center of this widget into the map
            bounds = view_tree["bounds"]
            center = [(bounds[0] + bounds[2]) / 2,
                      (bounds[1] + bounds[3]) / 2]
            self.idx.insert(self.global_drawing_order, (center[0], center[1], center[0], center[1]))
            
        self.global_drawing_order += 1
        child_with_drawing_orders = sorted(view_tree["children"], key=lambda x: x["drawing-order"])
        for child in child_with_drawing_orders:
            self.set_drawing_orders(view_tree=child)
    
    def filter_covered_view(self):
        for view in self.views:
            pass


if __name__ == '__main__':
    views = Uiautomator2_Helper().get_views()
    print(views)
