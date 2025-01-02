<div align="center">
<h1>Kea</h1>

 <a href='LICENSE'><img src='https://img.shields.io/badge/License-MIT-orange'></a> &nbsp;&nbsp;&nbsp;
 <a><img src='https://img.shields.io/badge/python-3.9, 3.10, 3.11, 3.12, 3.13-blue'></a> &nbsp;&nbsp;&nbsp;
 <a href='https://kea-technic-docs.readthedocs.io/zh-cn/latest/part-theory/introduction.html'><img src='https://img.shields.io/badge/doc-1.0.0-blue'></a>
</div>

<div align="center">
    <img src="kea/resources/kea_log(1).png" alt="kea_logo" style="border-radius: 18px"/>
</div>



### 简介

Kea 是一个通用的测试工具，通过[基于性质的测试](https://en.wikipedia.org/wiki/Software_testing#Property_testing) 发现移动（GUI）应用中的功能性错误。
Kea 目前支持 Android 和 HarmonyOS。


<p align="center">
  <img src="kea/resources/kea-platforms.jpg" width="300"/>
</p>

### 论文

📘 **[Kea's Paper @ ASE 2024 (ACM Distinguished Paper)](https://xyiheng.github.io//files/Property_Based_Testing_for_Android_Apps.pdf)**

> "General and Practical Property-based Testing for Android Apps". 
> Yiheng Xiong, Ting Su, Jue Wang, Jingling Sun, Geguang Pu, Zhendong Su.
> In ASE 2024. 

你可以在 [ECNU SE lab - mobile app analysis](https://mobile-app-analysis.github.io) 找到我们的相关工作。


### [演示视频](https://www.bilibili.com/video/BV1QPkoYREgh/?share_source=copy_web)

### Docs

[文档](https://kea-technic-docs.readthedocs.io/zh-cn/latest/part-theory/introduction.html)

[用户手册](https://kea-technic-docs.readthedocs.io/zh-cn/latest/part-keaUserManuel/envirnment_setup.html)

[设计手册](https://kea-technic-docs.readthedocs.io/zh-cn/latest/part-designDocument/intro.html)

[测试报告](https://kea-technic-docs.readthedocs.io/zh-cn/latest/part-experiment/exp.html)

[覆盖报告](https://xixianliang.github.io/kea-technic-docs/)


### 安装和使用

**环境配置**

- Python 3.9+
- `adb` or `hdc` cmd tools available
- Connect an Android / HarmonyOS device or emulator to your PC

[安卓/鸿蒙环境配置教程](https://kea-technic-docs.readthedocs.io/zh-CN/latest/part-keaUserManuel/envirnment_setup.html)

**工具安装**

输入以下命令安装 Kea。

```bash
git clone https://github.com/ecnusse/Kea.git
cd Kea
pip install -e .
```

**快速开始**

```
kea -f example/example_property.py -a example/omninotes.apk
```

### 作者/维护者

Kea的原作者是：
[Yiheng Xiong](https://xyiheng.github.io/), 
[Ting Su](http://tingsu.github.io/),
[Jue Wang](https://cv.juewang.info/),
[Jingling Sun](https://jinglingsun.github.io/),
[Geguang Pu](),
[Zhendong Su](https://people.inf.ethz.ch/suz/).

目前 Kea 的核心维护者：
[Xiangchen Shen](https://xiangchenshen.github.io/), 
[Xixian Liang](https://xixianliang.github.io/resume/),
[Mengqian Xu](), [Bo Ma]()

### Kea 参考的开源工具

- [Droidbot](https://github.com/honeynet/droidbot)
- [HMDroidbot](https://github.com/ecnusse/HMDroidbot)
- [hypothesis](https://github.com/HypothesisWorks/hypothesis)
- [hmdriver2](https://github.com/codematrixer/hmdriver2)
- [uiautomator2](https://github.com/openatx/uiautomator2)


### 相关阅读

<details>
  <summary>Relevant References for Kea</summary>

📘 An Empirical Study of Functional Bugs in Android Apps. ISSTA 2023. [pdf](https://dl.acm.org/doi/10.1145/3597926.3598138)

📘 Property-Based Testing for Validating User Privacy-Related Functionalities in Social Media Apps. FSE 2024. [pdf](https://dl.acm.org/doi/10.1145/3663529.3663863)

📘 Property-Based Fuzzing for Finding Data Manipulation Errors in Android Apps. ESEC/FSE 2023. [pdf](https://dl.acm.org/doi/10.1145/3611643.3616286)

📘 Characterizing and Finding System Setting-Related Defects in Android Apps. TSE 2023. [pdf](https://ieeexplore.ieee.org/document/10064083)

📘 Understanding and Finding System Setting-related Defects in Android Apps. ISSTA 2021. [pdf](https://dl.acm.org/doi/10.1145/3460319.3464806)

</details>

<details>
  <summary>References for Property-based Testing</summary>

📘 Property-Based Testing in Practice. ICSE 2024. [pdf](https://dl.acm.org/doi/10.1145/3597503.3639581)

📘 QuickCheck: a lightweight tool for random testing of Haskell programs. ICFP 2000. [pdf](https://dl.acm.org/doi/10.1145/357766.351266)

📘 Property-based testing: a new approach to testing for assurance. Software Engineering Notes 1997. [pdf](https://dl.acm.org/doi/pdf/10.1145/263244.263267)

</details>