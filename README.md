<div align="center">
<h1>Kea</h1>

<a href='https://dl.acm.org/doi/10.1145/3691620.3694986'><img src='https://img.shields.io/badge/acm-10.1145-blue.svg'></a> &nbsp;&nbsp;&nbsp;
 <a href='LICENSE'><img src='https://img.shields.io/badge/License-MIT-orange'></a> &nbsp;&nbsp;&nbsp;
 <a><img src='https://img.shields.io/badge/python-3.9, 3.10, 3.11, 3.12, 3.13-blue'></a> &nbsp;&nbsp;&nbsp;
 <a href='https://kea-doc.readthedocs.io/en/latest/'><img src='https://img.shields.io/badge/doc-1.0.0-blue'></a>
</div>

<div align="center">
    <img src="kea/resources/kea_log(1).png" alt="kea_logo" style="border-radius: 18px"/>
</div>

<p>

</p>

Kea is a general and practical testing tool based on the idea of [property-based testing](https://en.wikipedia.org/wiki/Software_testing#Property_testing) for finding functional bugs in mobile (GUI) apps.
Kea currently supports Android and HarmonyOS.

📘 **[Kea's Paper@ASE 2024](https://xyiheng.github.io//files/Property_Based_Testing_for_Android_Apps.pdf)**

> "General and Practical Property-based Testing for Android Apps". 
> Yiheng Xiong, Ting Su, Jue Wang, Jingling Sun, Geguang Pu, Zhendong Su.
> In ASE 2024. 

You can find more about our work on testing/analyzing mobile apps at this [website](https://mobile-app-analysis.github.io).

📘 **[User manual & Documentation](https://kea-doc.readthedocs.io/en/latest/)**


The apk file used in our evaluation can be downloaded from [here](https://drive.google.com/drive/folders/19Ysgnnwr1HDvrXBW7t1uYB_T7QdwkZKC?usp=sharing)

## Setup

Requirements:

- Python 3.9+
- `adb` cmd avaliable (Android SDK)
- An emulator or devices connected to your PC


You can input following commands to grep and install the required packages.

```bash
git clone https://github.com/ecnusse/Kea.git
cd Kea
pip install -e .
```

You can create an emulator before running Kea. See [this link](https://stackoverflow.com/questions/43275238/how-to-set-system-images-path-when-creating-an-android-avd) for how to create avd using [avdmanager](https://developer.android.com/studio/command-line/avdmanager).
The following sample command will help you create an emulator, which will help you start using Kea quickly：

```bash
sdkmanager "build-tools;29.0.3" "platform-tools" "platforms;android-29"
sdkmanager "system-images;android-29;google_apis;x86"
avdmanager create avd --force --name Android10.0 --package "system-images;android-29;google_apis;x86" --abi google_apis/x86 --sdcard 1024M --device "pixel_2"
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

### Relevant Tools Used in Kea

1. [droidbot](https://github.com/honeynet/droidbot)
2. [uiautomator2](https://github.com/openatx/uiautomator2)
3. [hmdriver2](https://github.com/codematrixer/hmdriver2)
4. [hypothesis](https://github.com/HypothesisWorks/hypothesis)

### Contributors/Maintainers

The original authors of Kea are:
[Yiheng Xiong](https://xyiheng.github.io/), 
[Ting Su](http://tingsu.github.io/),
[Jue Wang](https://cv.juewang.info/),
[Jingling Sun](https://jinglingsun.github.io/),
[Geguang Pu](),
[Zhendong Su](https://people.inf.ethz.ch/suz/)

Now we have additional active contributors:
[Xiangchen Shen](https://xiangchenshen.github.io/), 
[Xixian Liang](https://xixianliang.github.io/resume/),
[Mengqian Xu]()

### Relevant References for Kea

📘 An Empirical Study of Functional Bugs in Android Apps. ISSTA 2023. [pdf](https://dl.acm.org/doi/10.1145/3597926.3598138)

📘 Property-Based Testing for Validating User Privacy-Related Functionalities in Social Media Apps. FSE 2024. [pdf](https://dl.acm.org/doi/10.1145/3663529.3663863)

📘 Property-Based Fuzzing for Finding Data Manipulation Errors in Android Apps. ESEC/FSE 2023. [pdf](https://dl.acm.org/doi/10.1145/3611643.3616286)

📘 Characterizing and Finding System Setting-Related Defects in Android Apps. TSE 2023. [pdf](https://ieeexplore.ieee.org/document/10064083)

📘 Understanding and Finding System Setting-related Defects in Android Apps. ISSTA 2021. [pdf](https://dl.acm.org/doi/10.1145/3460319.3464806)


### References for Property-based Testing

📘 Property-Based Testing in Practice. ICSE 2024. [pdf](https://dl.acm.org/doi/10.1145/3597503.3639581)

📘 QuickCheck: a lightweight tool for random testing of Haskell programs. ICFP 2000. [pdf](https://dl.acm.org/doi/10.1145/357766.351266)

📘 Property-based testing: a new approach to testing for assurance. Software Engineering Notes 1997. [pdf](https://dl.acm.org/doi/pdf/10.1145/263244.263267)