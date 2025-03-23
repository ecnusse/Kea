<div align="center">
<h1>Kea</h1>

 <a href='LICENSE'><img src='https://img.shields.io/badge/License-MIT-orange'></a> &nbsp;&nbsp;&nbsp;
 <a><img src='https://img.shields.io/badge/python-3.8, 3.9, 3.10, 3.11, 3.12, 3.13-blue'></a> &nbsp;&nbsp;&nbsp;
 <a href='https://kea-docs.readthedocs.io/en/latest/part-theory/introduction.html'><img src='https://img.shields.io/badge/doc-1.0.0-blue'></a>
</div>

<div align="center">
    <img src="kea/resources/kea_log(1).png" alt="kea_logo" style="border-radius: 18px"/>
</div>


### Intro ([中文](README_CN.md))

Kea is a general and practical testing tool based on the idea of [property-based testing](https://en.wikipedia.org/wiki/Software_testing#Property_testing) for finding functional (logic) bugs in mobile (GUI) apps.
Kea currently supports Android and HarmonyOS.


<p align="center">
  <img src="kea/resources/kea-platforms.jpg" width="300"/>
</p>

### Publication 

📘 **[Kea's Paper @ ASE 2024 (won ACM Distinguished Paper Award!)](https://xyiheng.github.io//files/Property_Based_Testing_for_Android_Apps.pdf)**

> "General and Practical Property-based Testing for Android Apps". 
> Yiheng Xiong, Ting Su, Jue Wang, Jingling Sun, Geguang Pu, Zhendong Su.
> In ASE 2024. 

### Blogs (In Chinese)

[别再苦哈哈写测试脚本了，生成它们吧！(一)](https://mp.weixin.qq.com/s/R2kLCkXpDjpa8wCX4Eidtg)

[别再苦哈哈写测试脚本了，生成它们吧！(二)](https://mp.weixin.qq.com/s/s4WkdstNcKupu9OP8jeOXw)

[别再苦哈哈写测试脚本了，生成它们吧！(三)](https://mp.weixin.qq.com/s/BjXyo-xJRmPB_sCc4pmh8g)

### More Info

> Find more about our work on testing/analyzing mobile apps: [ECNU-SSE-Lab - Mobile App Analysis](https://mobile-app-analysis.github.io).

> A list of literature on mobile app testing and analysis: [Mobile App Analysis and Testing Literature](https://github.com/XYIheng/MobileAppTesting).


### [Demonstration Video](https://www.bilibili.com/video/BV1QPkoYREgh/?share_source=copy_web) (In Chinese)

### Docs

[Full Doc](https://kea-docs.readthedocs.io/en/latest/part-theory/introduction.html)

[User Manual](https://kea-docs.readthedocs.io/en/latest/part-keaUserManuel/envirnment_setup.html)

[Design Manual](https://kea-docs.readthedocs.io/en/latest/part-designDocument/intro.html)

[Test Report](https://kea-docs.readthedocs.io/en/latest/part-experiment/exp.html)

[Coverage Report](https://ecnusse.github.io/Kea/)


### Installation and Quickstart

**Prerequisites**

- Python 3.8+
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

**Note:** The LLM module is currently in an experimental phase. We are actively gathering feedback to improve its functionality and stability. We appreciate your understanding and support from the community, and we welcome any suggestions or comments.

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
[Mengqian Xu](https://mengqianx.github.io/)

### Relevant Tools Used in Kea

- [Droidbot](https://github.com/honeynet/droidbot)
- [HMDroidbot](https://github.com/ecnusse/HMDroidbot)
- [hypothesis](https://github.com/HypothesisWorks/hypothesis)
- [hmdriver2](https://github.com/codematrixer/hmdriver2)
- [uiautomator2](https://github.com/openatx/uiautomator2)


### References


#### Relevant References for Kea


> 📘 General and Practical Property-based Testing for Android Apps. ASE 2024. [pdf](https://dl.acm.org/doi/10.1145/3691620.3694986)

> 📘 Property-Based Testing for Validating User Privacy-Related Functionalities in Social Media Apps. FSE 2024. [pdf](https://dl.acm.org/doi/10.1145/3663529.3663863)

> 📘 An Empirical Study of Functional Bugs in Android Apps. ISSTA 2023. [pdf](https://dl.acm.org/doi/10.1145/3597926.3598138)

> 📘 Property-Based Fuzzing for Finding Data Manipulation Errors in Android Apps. ESEC/FSE 2023. [pdf](https://dl.acm.org/doi/10.1145/3611643.3616286)

> 📘 Characterizing and Finding System Setting-Related Defects in Android Apps. TSE 2023. [pdf](https://ieeexplore.ieee.org/document/10064083)

> 📘 Understanding and Finding System Setting-related Defects in Android Apps. ISSTA 2021. [pdf](https://dl.acm.org/doi/10.1145/3460319.3464806)

> 📘 Fully Automated Functional Fuzzing of Android Apps for Detecting Non-Crashing Logic Bugs. OOPSLA 2021. [pdf](https://dl.acm.org/doi/10.1145/3485533)

</details>

<details>
  <summary>References for Property-based Testing</summary>

📘 Property-Based Testing in Practice. ICSE 2024. [pdf](https://dl.acm.org/doi/10.1145/3597503.3639581)

📘 QuickCheck: a lightweight tool for random testing of Haskell programs. ICFP 2000. [pdf](https://dl.acm.org/doi/10.1145/357766.351266)

📘 Property-based testing: a new approach to testing for assurance. Software Engineering Notes 1997. [pdf](https://dl.acm.org/doi/pdf/10.1145/263244.263267)

</details>
