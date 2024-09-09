# Kea
![logo](kea/resources/kea_log(1).png)

Kea is a general and practical testing tool based on the idea of property-based testing for finding functional bugs in Android apps.

📘 [Documentation](https://droidchecker-doc.readthedocs.io/en/latest/)

The apk file used in our evaluation can be downloaded from [here](https://drive.google.com/drive/folders/19Ysgnnwr1HDvrXBW7t1uYB_T7QdwkZKC?usp=sharing)
## Setup

Requirements:

- Python 3.8+
- Android SDK

You can input following commands to grep and install the required packages.

```bash
git clone https://github.com/ecnusse/Kea.git
cd home
pip install -e .
```

>**Tips:**   
> Before you run the commands to create an emulator, you should pay attention to the hardware virtualization:  
> - For `Windows`  
>   You can run our Kea on Windows directly.  
>   You should make sure `Intel VT-x` or `AMD-V` is enabled in `BIOS/UEFI`.  
>   If your Windows supports `Hyper-V` and you have enabled this feature before, you may need to disable `Hyper-V` because `Hyper-V` will conflict with other virtualization software.
> - For `Mac OS`  
>   The hardware virtualization function is already built-in and enabled, so no additional configuration is required by users.
> - For `Linux`  
>   You should make sure `Intel VT-x` or `AMD-V` is enabled in `BIOS/UEFI`.  
> 
> If you are willing to use virtual machine to run our Kea, This still works. You just need to enable your vm can use hardware virtualization.  
> Take `Windows` as an example, if you like to use Linux system for developing instead of using windows directly. we recommend you to use [WSL2](https://ubuntu.com/desktop/wsl) to run Kea. This may can help you run Kea more fluently than [Vmware](https://www.vmware.com/products/desktop-hypervisor/workstation-and-fusion) and [VirtualBox](https://www.virtualbox.org/).  
>> Using [WSL2](https://ubuntu.com/desktop/wsl) to run emulator need you to enable `Hyper-V`, but `Hyper-V` is only available in `Windows Professional\Enterprise\Education` editions.  


You can create an emulator before running Kea. See [this link](https://stackoverflow.com/questions/43275238/how-to-set-system-images-path-when-creating-an-android-avd) for how to create avd using [avdmanager](https://developer.android.com/studio/command-line/avdmanager).
The following sample command will help you create an emulator, which will help you start using Kea quickly：

```bash
sdkmanager "build-tools;29.0.3" "platform-tools" "platforms;android-29"
sdkmanager "system-images;android-29;google_apis;x86"
avdmanager create avd --force --name Android10.0 --package 'system-images;android-29;google_apis;x86' --abi google_apis/x86 --sdcard 1024M --device "pixel_2"
```

Next, you can start one emulator and assign their port numbers with the following commands:

```bash
emulator -avd Android10.0 -read-only -port 5554
```


## Getting Started

### Quick example

If you have downloaded our project and configured the environment, you only need to enter "example/" to execute our sample property with the following command:

```
kea -f example.py -a omninotes.apk
```

That's it! You can see the test results in the "output" directory.

#### Bug report

The ``bug_report.html`` file in the output directory contains the bug report. You can see the details of the bug in this file.
You can use the browser (Google Chrome, Firefox, etc.) to open this file.
In the bug report, you can see the following information:

1. The screenshots of the execution trace. It shows the UI state of the app during the test, which can help you identify and reproduce the bug. Under each screenshot, you can see the event index and the event type (e.g., click, long click) that executed on the UI state.
2. The bug link list. It shows the bug link of the bug. You can click the link to jump to the first state of the property that caused the bug.

### Optional arguments

Kea provides the following options. please consult ``kea -h`` for a full list.

``-f``: The test files that contain the properties.

``-a --apk``: The apk file of the app under test.

``-d --device_serial``: The serial number of the device used in the test. (use 'adb devices' to find)

``-o --output``: The output directory of the execution results.

``-p --policy``: The policy name of the exploration. ("random" or "mutate")

``-t --timeout``: The maximum testing time.

``-n``: Every n events, then restart the app.

``-m --main_path``: the file of the main path.

### Specify your properties

A property in Kea consists of three parts: A function that looks like a normal test, a `@rule` decorator that specifies this function as a property, and a ``@precondition`` decorator that specifies the precondition of the property.

Here is an example of a property:

```python
@precondition(lambda self: d(resourceId="it.feio.android.omninotes.alpha:id/search_src_text").exists())
@rule()
def search_bar_should_exist_after_rotation(self):
    d.rotate('l')
    d.rotate('n')
    assert d(resourceId="it.feio.android.omninotes.alpha:id/search_src_text").exists() 
```

This is an example property from OmniNotes. The property checks if the search exists after rotating the device. The property is defined as a function `search_bar_should_exist_after_rotation`. The function contains the test logic. The `@rule` decorator specifies this function as a property.

Note that we use the `@precondition` decorator to specify the precondition of the property. The precondition is a lambda function that returns a boolean value. If the lambda function returns `True`, the property will be executed. Otherwise, the property will be skipped.

To run this property, we need to define a test class that inherits from ``Kea``. Then put this property in the test class

Finally, we can run the property by executing the following command:

```bash
kea -f [property_file_name] -a [apk_file_name]
```

where ``property_file_name`` is the name of the property file.

#### How to get the attribute of the UI object

To get the attribute of the UI object, you can use the tool [weditor](https://github.com/alibaba/web-editor).

```bash
pip install weditor
weditor
```

Then, you can connect the device and get the attribute of the UI object.

### API Documents

### UI events

Note that currently, we use [uiautomator2](https://github.com/openatx/uiautomator2) to interact with the app. You can find more information in [uiautomator2](https://github.com/openatx/uiautomator2).
You can also use other tools to interact with the app, which can be easily implemented by modifying the `main.py`.

For example, to send the click event to the app, you can use the following code:

```python
d(resourceId="player_playback_button").click()
```

``d`` is the object of the uiautomator2.
``resourceId`` sets the resource id of the element.
``click()`` sends the click event to the element.

Here are some common operations:

* click
  ```python
  d(text="OK").click()
  ```
* long_click
  ```python
  d(text="OK").long_click()
  ```
* edit text
  ```python
  d(text="OK").set_text("text")
  ```
* rotate device
  ```python
  d.rotate("l") # or left
  d.rotate("r") # or right
  ```
* press [key]
  ```python
  d.press("home")
  d.press("back")
  ```

We use selector to identify the UI object in the current window.

**Selector**(you can also look at [uiautomator2](https://github.com/openatx/uiautomator2?tab=readme-ov-file#selector))Selector is a handy mechanism to identify a specific UI object in the current window.Selector supports below parameters.

* `text`, `textContains`, `textMatches`, `textStartsWith`
* `className`, `classNameMatches`
* `description`, `descriptionContains`, `descriptionMatches`, `descriptionStartsWith`
* `checkable`, `checked`, `clickable`, `longClickable`
* `scrollable`, `enabled`,`focusable`, `focused`, `selected`
* `packageName`, `packageNameMatches`
* `resourceId`, `resourceIdMatches`
* `index`, `instance`

### initialize

We use ``@initialize`` to pass the welcome page or the login page of the app.
For example, in OmniNotes, we can use ``@initialize`` to specify a function and wrtite the corresponding UI events to pass the welcome page.

```python
@initialize()
def pass_welcome_pages(self):
    # click next button 5 times
    for _ in range(5):
        d(resourceId="it.feio.android.omninotes.alpha:id/next").click()
    # click done button
    d(resourceId="it.feio.android.omninotes.alpha:id/done").click()
```

The, after testing started, this function will be executed first to pass the welcome page.

### Run multiple properties together

Suppose we have several properties in different files, we can run them together by specifying multiple files in the command line.

```bash
kea -f [property_file_name1] [property_file_name2] -a [apk_file_name]
```

## Bug list found by Kea

* OmniNotes: [#942](https://github.com/federicoiosue/Omni-Notes/issues/942), [#946](https://github.com/federicoiosue/Omni-Notes/issues/946), [#948](https://github.com/federicoiosue/Omni-Notes/issues/948), [#949](https://github.com/federicoiosue/Omni-Notes/issues/949), [#950](https://github.com/federicoiosue/Omni-Notes/issues/950), [#951](https://github.com/federicoiosue/Omni-Notes/issues/951), [#954](https://github.com/federicoiosue/Omni-Notes/issues/954), [#956](https://github.com/federicoiosue/Omni-Notes/issues/956), [#939](https://github.com/federicoiosue/Omni-Notes/issues/939), [#981](https://github.com/federicoiosue/Omni-Notes/issues/981), [#937](https://github.com/federicoiosue/Omni-Notes/issues/937), [#938](https://github.com/federicoiosue/Omni-Notes/issues/938), [#938](https://github.com/federicoiosue/Omni-Notes/issues/937), [#939](https://github.com/federicoiosue/Omni-Notes/issues/937), [#940](https://github.com/federicoiosue/Omni-Notes/issues/940), [#941](https://github.com/federicoiosue/Omni-Notes/issues/941), [#945](https://github.com/federicoiosue/Omni-Notes/issues/945),
* Markor: [#2153](https://github.com/gsantner/markor/issues/2153), [#2196](https://github.com/gsantner/markor/issues/2196), [#2197](https://github.com/gsantner/markor/issues/2197), [#2198](https://github.com/gsantner/markor/issues/2198), [#2199](https://github.com/gsantner/markor/issues/2199), [#2250](https://github.com/gsantner/markor/issues/2250)
* AmazeFileManager: [#3991](https://github.com/TeamAmaze/AmazeFileManager/issues/3991), [#4016](https://github.com/TeamAmaze/AmazeFileManager/issues/4016), [#4130](https://github.com/TeamAmaze/AmazeFileManager/issues/4130)
* AnkiDroid: [#15993](https://github.com/ankidroid/Anki-Android/issues/15993), [#15995](https://github.com/ankidroid/Anki-Android/issues/15995)
* transistor: [#488](https://codeberg.org/y20k/transistor/issues/488), [#489](https://codeberg.org/y20k/transistor/issues/489), [#495](https://codeberg.org/y20k/transistor/issues/495)
* Simpletask: [#1230](https://github.com/mpcjanssen/simpletask-android/issues/1230)

# Acknowledgement

1. [droidbot](https://github.com/honeynet/droidbot)
2. [uiautomator2](https://github.com/openatx/uiautomator2)
