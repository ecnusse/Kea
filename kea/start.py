import argparse
import warnings
from dataclasses import dataclass

from hypothesis.errors import NonInteractiveExampleWarning
warnings.filterwarnings("ignore", category=NonInteractiveExampleWarning)
import coloredlogs
coloredlogs.install()

from .input_manager import DEFAULT_POLICY, DEFAULT_TIMEOUT
from .kea import Kea
from .utils import get_yml_config, sanitize_args
from .droidbot import DroidBot
from .utils import DEFAULT_POLICY, DEFAULT_EVENT_INTERVAL, DEFAULT_TIMEOUT, DEFAULT_EVENT_COUNT

@dataclass
class Setting:
    """`Setting` is a Python DataClass

    TODO: it seems the Setting class is redudant? why not just using options?
    """
    apk_path: str
    device_serial: str = None
    output_dir:str ="output"
    is_emulator: bool =True     #True for emulators, False for real devices.
    policy_name: str = DEFAULT_POLICY
    random_input: bool =True
    script_path: str=None
    event_interval: int= DEFAULT_EVENT_INTERVAL
    timeout: int = DEFAULT_TIMEOUT
    event_count: int= DEFAULT_EVENT_COUNT
    cv_mode=None
    debug_mode: bool=False
    keep_app:bool=None
    keep_env=None
    profiling_method=None
    grant_perm: bool=True
    send_document: bool=True
    enable_accessibility_hard=None
    master=None
    humanoid=None
    ignore_ad=None
    replay_output=None
    number_of_events_that_restart_app:int =100
    run_initial_rules_after_every_mutation=True
    is_harmonyos:bool=False
    generate_utg:bool=False
    is_package:bool=False

def parse_args():
    """Parse, load and sanitize the args from the command line and the config file `config.yml`.

    The args are either specified via the command line or the config file `config.yml`.
    The design purpose of config.yml is to ease specifying the args via a config file.
    """
    parser = argparse.ArgumentParser(description="Start kea to test app.",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-f", nargs="+", action="store",dest="property_files", help="The app properties to be tested.")
    parser.add_argument("-d", "--device_serial", action="store", dest="device_serial", default=None,
                        help="The serial number of target device (use `adb devices` to find)")
    parser.add_argument("-a","--apk", action="store", dest="apk_path",
                        help="The file path to target APK")
    parser.add_argument("-o","--output", action="store", dest="output_dir", default="output",
                        help="directory of output")
    parser.add_argument("-p","--policy", action="store", dest="policy",choices=["random", "guided", "llm"], default=DEFAULT_POLICY,  # tingsu: can we change "mutate" to "guided"?
                        help='Policy used for input event generation. ')
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
    parser.add_argument("-is_harmonyos", action="store_true", dest="is_harmonyos", default=False,
                        help="use harmonyos devices")
    parser.add_argument("-load_config", action="store_true", dest="load_config", default=False,
                        help="load the args from config.yml, and the args in the command line will be ignored.")
    parser.add_argument("-utg", action="store_true", dest="generate_utg", default=False,
                        help="Generate UI transition graph")
    options = parser.parse_args()

    # load the args from the config file `config.yml`
    if options.load_config:
        options = load_ymal_args(options)

    # sanitize these args
    sanitize_args(options) 

    return options

def load_ymal_args(opts):
    """Load the args from the config file `config.yml`. 

    The design purpose of config.yml is to ease specifying the args via a config file.
    Note that the values of the args in config.yml would overwrite those args specified via the command line.
    """
    config_dict = get_yml_config()
    for key, value in config_dict.items():
        if key.lower() == "system" and value:
            opts.is_harmonyos = value.lower() == "harmonyos"
        elif key.lower() in ["app_path", "package", "package_name"] and value:
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
            opts.property_files = value
    
    return opts

def load_pdl_driver(settings: "Setting"):
    """Load the pdl (property description language) driver according to the target mobile platform
        (e.g., Android, HarmonyOS).
    """
    if settings.is_harmonyos:
        from kea.harmonyos_pdl_driver import HarmonyOS_PDL_Driver
        return HarmonyOS_PDL_Driver(serial=settings.device_serial)
    else:
        from kea.android_pdl_driver import Android_PDL_Driver
        return Android_PDL_Driver(serial=settings.device_serial)
    
def start_kea(kea:"Kea", settings:"Setting" = None):

    # droidbot is used as the data generator of Kea
    droidbot = DroidBot(    
        app_path=settings.apk_path,
        device_serial=settings.device_serial,
        is_emulator=settings.is_emulator,
        output_dir=settings.output_dir,
        env_policy = None,
        policy_name=settings.policy_name,
        random_input=settings.random_input,
        script_path=settings.script_path,
        event_interval=settings.event_interval,
        timeout=settings.timeout,
        event_count=settings.event_count,
        cv_mode=settings.cv_mode,
        debug_mode=settings.debug_mode,
        keep_app=settings.keep_app,
        keep_env=settings.keep_env,
        profiling_method=settings.profiling_method,
        grant_perm=settings.grant_perm,
        send_document=settings.send_document,
        enable_accessibility_hard=settings.enable_accessibility_hard,
        master=settings.master,
        humanoid=settings.humanoid,
        ignore_ad=settings.ignore_ad,
        replay_output=settings.replay_output,
        kea=kea,
        number_of_events_that_restart_app=settings.number_of_events_that_restart_app,
        run_initial_rules_after_every_mutation=settings.run_initial_rules_after_every_mutation,
        is_harmonyos=settings.is_harmonyos,
        is_package=settings.is_package,
        settings=settings,
        generate_utg=settings.generate_utg
    )

    kea._pdl_driver.set_droidbot(droidbot)  
    droidbot.start()
    

def main():
    """the main entry of Kea.
    """
    # parse the args
    options = parse_args()

    # setup the setting
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
                       is_emulator=options.is_emulator,
                       generate_utg=options.generate_utg
                       )
    
    # load the pdl driver for Android/HarmonyOS
    driver = load_pdl_driver(settings)
    Kea.set_pdl_driver(driver)
    # load the app properties to be tested
    Kea.load_app_properties(options.property_files)

    # create Kea
    kea = Kea()
    print(f"INFO: All Test cases: {kea._KeaTest_DB}") 
    # start Kea
    start_kea(kea, settings) 

if __name__ == "__main__":
    main()