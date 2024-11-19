<div align="center">
<h1>Kea</h1>

<a href='https://dl.acm.org/doi/10.1145/3691620.3694986'><img src='https://img.shields.io/badge/acm-10.1145-blue.svg'></a> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
 <a href='LICENSE'><img src='https://img.shields.io/badge/License-MIT-blue'></a>
</div>

<div align="center">
    <img src="kea/resources/kea_log(1).png" alt="kea_logo" style="border-radius: 18px"/>
</div>

<p>

</p>

Kea is a general and practical testing tool based on the idea of [property-based testing](https://en.wikipedia.org/wiki/Software_testing#Property_testing) for finding functional bugs in mobile (GUI) apps.
Kea currently supports Android and is planned to support HarmonyOS soon.

📘 [Kea's Paper@ASE 2024](https://xyiheng.github.io//files/Property_Based_Testing_for_Android_Apps.pdf)

> "General and Practical Property-based Testing for Android Apps". 
> Yiheng Xiong, Ting Su, Jue Wang, Jingling Sun, Geguang Pu, Zhendong Su.
> In ASE 2024. 

You can find more about our work on testing/analyzing mobile apps at this [website](https://mobile-app-analysis.github.io).

📘 [User manual & Documentation](https://kea-doc.readthedocs.io/en/latest/)


The apk file used in our evaluation can be downloaded from [here](https://drive.google.com/drive/folders/19Ysgnnwr1HDvrXBW7t1uYB_T7QdwkZKC?usp=sharing)

## Setup

Requirements:

- Python 3.8+
- Android SDK

You can input following commands to grep and install the required packages.

```bash
git clone https://github.com/ecnusse/Kea.git
cd Kea
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
>> Using [WSL2](https://ubuntu.com/desktop/wsl) to run emulator need you to enable `Hyper-V`, here we recommend you to use Windows 11.  


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


## Functional bugs found by Kea

* OmniNotes: [#942](https://github.com/federicoiosue/Omni-Notes/issues/942), [#946](https://github.com/federicoiosue/Omni-Notes/issues/946), [#948](https://github.com/federicoiosue/Omni-Notes/issues/948), [#949](https://github.com/federicoiosue/Omni-Notes/issues/949), [#950](https://github.com/federicoiosue/Omni-Notes/issues/950), [#951](https://github.com/federicoiosue/Omni-Notes/issues/951), [#954](https://github.com/federicoiosue/Omni-Notes/issues/954), [#956](https://github.com/federicoiosue/Omni-Notes/issues/956), [#939](https://github.com/federicoiosue/Omni-Notes/issues/939), [#981](https://github.com/federicoiosue/Omni-Notes/issues/981), [#937](https://github.com/federicoiosue/Omni-Notes/issues/937), [#938](https://github.com/federicoiosue/Omni-Notes/issues/938), [#938](https://github.com/federicoiosue/Omni-Notes/issues/937), [#939](https://github.com/federicoiosue/Omni-Notes/issues/937), [#940](https://github.com/federicoiosue/Omni-Notes/issues/940), [#941](https://github.com/federicoiosue/Omni-Notes/issues/941), [#945](https://github.com/federicoiosue/Omni-Notes/issues/945),
* Markor: [#2153](https://github.com/gsantner/markor/issues/2153), [#2196](https://github.com/gsantner/markor/issues/2196), [#2197](https://github.com/gsantner/markor/issues/2197), [#2198](https://github.com/gsantner/markor/issues/2198), [#2199](https://github.com/gsantner/markor/issues/2199), [#2250](https://github.com/gsantner/markor/issues/2250)
* AmazeFileManager: [#3991](https://github.com/TeamAmaze/AmazeFileManager/issues/3991), [#4016](https://github.com/TeamAmaze/AmazeFileManager/issues/4016), [#4130](https://github.com/TeamAmaze/AmazeFileManager/issues/4130)
* AnkiDroid: [#15993](https://github.com/ankidroid/Anki-Android/issues/15993), [#15995](https://github.com/ankidroid/Anki-Android/issues/15995)
* transistor: [#488](https://codeberg.org/y20k/transistor/issues/488), [#489](https://codeberg.org/y20k/transistor/issues/489), [#495](https://codeberg.org/y20k/transistor/issues/495)
* Simpletask: [#1230](https://github.com/mpcjanssen/simpletask-android/issues/1230)


# Maintainers

[Yiheng Xiong](https://xyiheng.github.io/), 
[Xiangcheng Shen](https://xiangchenshen.github.io/), 
[Xixian Liang](https://xixianliang.github.io/resume/),
[Ting Su](http://tingsu.github.io/)


# Relevant Tools

1. [droidbot](https://github.com/honeynet/droidbot)
2. [uiautomator2](https://github.com/openatx/uiautomator2)
3. [hmdriver2](https://github.com/codematrixer/hmdriver2)
4. [hypothesis](https://github.com/HypothesisWorks/hypothesis)
