from typing import (
    Any,
    Callable,
    Dict,
    List
)

from kea import env_manager, input_manager
from kea.droidbot import DroidBot
from kea.kea import Kea
from copy import copy
from hypothesis.errors import NonInteractiveExampleWarning
import warnings
from dataclasses import dataclass
from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
    from kea.pdl import PDL as Android_PDL
    from kea.pdl_hm import PDL as HarmonyOS_PDL

from .property_decorator import rule, precondition, initializer, mainPath

warnings.filterwarnings("ignore", category=NonInteractiveExampleWarning)
import coloredlogs
coloredlogs.install()

@dataclass
class Setting:
    apk_path: str
    device_serial: str ="emulator-5554"
    output_dir:str ="output"
    is_emulator: bool =True     #True for emulator, false for real device.
    policy_name: str =input_manager.DEFAULT_POLICY
    random_input: bool =True
    script_path: str=None
    event_interval: int=input_manager.DEFAULT_EVENT_INTERVAL
    timeout: int =input_manager.DEFAULT_TIMEOUT
    event_count: int=input_manager.DEFAULT_EVENT_COUNT
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

OUTPUT_DIR = "output"
d:Union["Android_PDL", "HarmonyOS_PDL"] | None = None

def start_kea(kea:"Kea", settings:"Setting" = None):
    # if settings is None:
    #     settings = kea.TestCase.settings

    droidbot = DroidBot(    # tingsu: why not naming "droid" as "droidbot"?
        app_path=settings.apk_path,
        device_serial=settings.device_serial,
        is_emulator=settings.is_emulator,
        output_dir=settings.output_dir,
        env_policy=env_manager.POLICY_NONE,
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
        is_harmonyos=settings.is_harmonyos
    )

    global d
    d = settings.d

    d.set_device_serial(settings.device_serial)
    d.set_droidbot(droidbot)
    droidbot.start()