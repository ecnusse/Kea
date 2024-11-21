from .input_manager import DEFAULT_DEVICE_SERIAL, DEFAULT_POLICY, DEFAULT_TIMEOUT
from .main import Kea, Setting, start_kea
from .utils import get_yml_config

import importlib
import os
import argparse
import sys
def parse_args():
    parser = argparse.ArgumentParser(description="Start kea to test app.",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-f",nargs="+", action="store",dest="files", help="The python files to be tested.")
    parser.add_argument("-d", "--device_serial", action="store", dest="device_serial", default=DEFAULT_DEVICE_SERIAL,
                        help="The serial number of target device (use `adb devices` to find)")
    parser.add_argument("-a","--apk", action="store", dest="apk_path",
                        help="The file path to target APK")
    parser.add_argument("-o","--output", action="store", dest="output_dir", default="output",
                        help="directory of output")
    parser.add_argument("-p","--policy", action="store", dest="policy",choices=["random", "guided"], default=DEFAULT_POLICY,  # tingsu: can we change "mutate" to "guided"?
                        help='Policy to use for test input generation. ')
    parser.add_argument("-t", "--timeout", action="store", dest="timeout", default=DEFAULT_TIMEOUT, type=int,
                        help="Timeout in seconds. Default: %d" % DEFAULT_TIMEOUT)
    parser.add_argument("-n","--number_of_events_that_restart_app", action="store", dest="number_of_events_that_restart_app", default=100, type=int,
                        help="Restart the app when this number of events has been executed. Default: 100")
    parser.add_argument("-debug", action="store_true", dest="debug_mode",
                        help="Run in debug mode (dump debug messages).")
    parser.add_argument("-keep_app", action="store_true", dest="keep_app",
                        help="Keep the app on the device after testing.")
    parser.add_argument("-grant_perm", action="store_true", dest="grant_perm",
                        help="Grant all permissions while installing. Useful for Android 6.0+.")
    parser.add_argument("-is_emulator", action="store_true", dest="is_emulator",default=True,
                        help="Declare the target device to be an emulator, which would be treated specially.")
    options = parser.parse_args()
    return options

def parse_ymal_args(opts):
    config_dict = get_yml_config()
    for key, value in config_dict.items():
        if key.lower() == "system" and value:
            opts.is_harmonyos = value.lower() == "harmonyos"
        elif key.lower() == "app_path" and value:
            opts.apk_path = value
        elif key.lower() == "policy" and value:
            opts.policy = value
        elif key.lower() == "output_dir" and value:
            opts.output_dir = value
        elif key.lower() == "count" and value:
            opts.count = value
        elif key.lower() in ["target", "device", "device_serial"] and value:
            opts.device_serial = value
        elif key.lower() in ["property", "properties", "file", "files"] and value:
            opts.files = value
    
    return opts


def import_and_instantiate_classes(files, settings:"Setting")->"Kea":
    workspace_path = os.path.abspath(os.getcwd())
    
    d = get_mobile_driver(settings)
    settings.d = d

    for file in files:
        
        file_abspath = os.path.join(workspace_path, file) if not os.path.isabs(file) else file
        
        module_dir = os.path.dirname(file_abspath)
        
        if module_dir not in sys.path:
            sys.path.insert(0, module_dir)
        
        if not os.path.exists(file_abspath):
            raise FileNotFoundError(f"{file} not exists.") 
        
        os.chdir(os.path.dirname(file_abspath))

        module_name, extension_name = [str(_) for _ in os.path.splitext(os.path.basename(file_abspath))]
        if not extension_name == ".py":
            raise AttributeError(f"{file} is not a property. It should be a .py file")
        
        try:
            # print(f"Importting module {module_name}")
            module = importlib.import_module(module_name)
            module.d = d

            # Find all classes in the module and attempt to instantiate them.
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, Kea) and attr is not Kea:
                    kea_core = Kea(attr)
        except ModuleNotFoundError as e:
            print(f"Error importing module {module_name}: {e}")
        
    os.chdir(workspace_path)
    return Kea()

def get_mobile_driver(settings:"Setting"):
    # initialize the dsl according to the system
    if not settings.is_harmonyos:
        from kea.dsl import Mobile
        return Mobile()
    else:
        from kea.dsl_hm import Mobile
        return Mobile(serial=settings.device_serial)

def main():
    options = parse_args()
    options = parse_ymal_args(options)
    # test_classes = []
    settings =  Setting(apk_path=options.apk_path,
                       device_serial=options.device_serial,
                       output_dir=options.output_dir,
                       timeout=options.timeout,
                       policy_name=options.policy,
                       number_of_events_that_restart_app=options.number_of_events_that_restart_app,  # tingsu: do we need a better name?
                       debug_mode=options.debug_mode,
                       keep_app=options.keep_app,
                       is_harmonyos=options.is_harmonyos,
                       grant_perm=options.grant_perm,
                       is_emulator=options.is_emulator
                       )
    if options.files is not None:
        kea_core = import_and_instantiate_classes(options.files, settings)
    print(f"Test cases: {kea_core._all_testCase}")
    start_kea(kea_core, settings)

if __name__ == "__main__":
    main()
    

    
