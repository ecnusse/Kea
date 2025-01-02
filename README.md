<div align="center">
<h1>Kea</h1>

 <a href='LICENSE'><img src='https://img.shields.io/badge/License-MIT-orange'></a> &nbsp;&nbsp;&nbsp;
 <a><img src='https://img.shields.io/badge/python-3.9, 3.10, 3.11, 3.12, 3.13-blue'></a> &nbsp;&nbsp;&nbsp;
 <a href='https://kea-technic-docs.readthedocs.io/zh-cn/latest/part-theory/introduction.html'><img src='https://img.shields.io/badge/doc-1.0.0-blue'></a>
</div>

<div align="center">
    <img src="kea/resources/kea_log(1).png" alt="kea_logo" style="border-radius: 18px"/>
</div>


### Intro 

Kea is a general and practical testing tool based on the idea of [property-based testing](https://en.wikipedia.org/wiki/Software_testing#Property_testing) for finding functional bugs in mobile (GUI) apps.
Kea currently supports Android and HarmonyOS.


<p align="center">
  <img src="kea/resources/kea-platforms.jpg" width="300"/>
</p>

### Publication 

📘 **[Kea's Paper @ ASE 2024 (ACM Distinguished Paper)](https://xyiheng.github.io//files/Property_Based_Testing_for_Android_Apps.pdf)**

> "General and Practical Property-based Testing for Android Apps". 
> Yiheng Xiong, Ting Su, Jue Wang, Jingling Sun, Geguang Pu, Zhendong Su.
> In ASE 2024. 

You can find more about our work on testing/analyzing mobile apps at this [ECNU SE lab - mobile app analysis](https://mobile-app-analysis.github.io).


### [Demonstration Video (Chinese)](https://www.bilibili.com/video/BV1QPkoYREgh/?share_source=copy_web)

### Docs

[Full Doc](https://kea-technic-docs.readthedocs.io/zh-cn/latest/part-theory/introduction.html)

[User Manual](https://kea-technic-docs.readthedocs.io/zh-cn/latest/part-keaUserManuel/envirnment_setup.html)

[Design Manual](https://kea-technic-docs.readthedocs.io/zh-cn/latest/part-designDocument/intro.html)

[Test Report](https://kea-technic-docs.readthedocs.io/zh-cn/latest/part-experiment/exp.html)

[Coverage Report](https://xixianliang.github.io/kea-technic-docs/)


### Installation and Quickstart

**Prerequisites**

- Python 3.9+
- `adb` or `hdc` cmd tools available
- Connect an Android / HarmonyOS device or emulator to your PC

[The setup guide for Android / HarmonyOS envirnments.](https://kea-technic-docs.readthedocs.io/en/latest/part-keaUserManuel/envirnment_setup.html)

**Installation**

Enter the following commands to install kea.

```bash
git clone https://github.com/ecnusse/Kea.git
cd Kea
pip install -e .
```

**Quick Start**

```
kea -f example/example_property.py -a example/omninotes.apk
```

### Contributors/Maintainers

The original authors of Kea are:
[Yiheng Xiong](https://xyiheng.github.io/), 
[Ting Su](http://tingsu.github.io/),
[Jue Wang](https://cv.juewang.info/),
[Jingling Sun](https://jinglingsun.github.io/),
[Geguang Pu](),
[Zhendong Su](https://people.inf.ethz.ch/suz/).

Now we have additional active contributors:
[Xiangchen Shen](https://xiangchenshen.github.io/), 
[Xixian Liang](https://xixianliang.github.io/resume/),
[Mengqian Xu]()

### References

- [Droidbot](https://github.com/honeynet/droidbot)

- [HMDroidbot](https://github.com/ecnusse/HMDroidbot)

- [hypothesis](https://github.com/HypothesisWorks/hypothesis)

- [hmdriver2](https://github.com/codematrixer/hmdriver2)

- [uiautomator2](https://github.com/openatx/uiautomator2)