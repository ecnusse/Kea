<div align="center">
<h1>Kea - 基于性质的移动操作系统应用自动化功能测试工具</h1>

 <a href='LICENSE'><img src='https://img.shields.io/badge/License-MIT-orange'></a> &nbsp;&nbsp;&nbsp;
 <a><img src='https://img.shields.io/badge/python-3.9, 3.10, 3.11, 3.12, 3.13-blue'></a> &nbsp;&nbsp;&nbsp;
 <a href='https://kea-technic-docs.readthedocs.io/zh-cn/latest/part-theory/introduction.html'><img src='https://img.shields.io/badge/doc-1.0.0-blue'></a>
</div>

<div align="center">
    <img src="kea/resources/kea_log(1).png" alt="kea_logo" style="border-radius: 18px"/>
</div>

### 参赛赛道

OS应用开发赛道

基于开源操作系统开发系统工具：系统功能测试工具。

### 参赛队伍信息

**学校：** 华东师范大学、江苏大学

**队伍：** 熊字有三横，一横一横又一横

**队员：** 梁锡贤、沈祥臣、马搏

**指导老师：** 苏亭、陈良育


### 项目背景

尽管存在各种移动应用的自动化测试工具，但是因为缺少测试预言，移动应用的自动化功能测试一直是一个具有挑战性的问题。基于性质的测试（Property-Based Testing，PBT）是一种自动化测试方法。该方法以被测系统应满足的行为性质为测试断言， 通过自动生成大量随机输入数据验证这些性质是否在各种情况下保持正确来检测被测系统中的缺陷。 与传统测试相比，基于性质的测试能够高效有效地覆盖被测系统输入空间及其边缘情况（corner cases），对被测软件实施深度功能测试，发现被测应用中潜在的缺陷。

Kea是一款基于PBT开发的移动应用自动化功能测试工具，支持根据选择的探索策略自动生成事件序列来达到应用更深层的状态,进而能够有效地覆盖移动应用事件空间。 值得一提的是，Kea针对性质定义是实施基于性质的测试的主要困难这一问题，设计了自定义的性质描述语言PDL，支持用户编写应用性质的前置条件、交互场景以及后置条件的检查， 可以有效降低实施基于性质的测试的难度，提升了基于性质的测试在移动应用开发中落地使用的可行性。

### 工具文档

[工具文档](https://kea-technic-docs.readthedocs.io/zh-cn/latest/part-theory/introduction.html)

[设计文档](https://kea-technic-docs.readthedocs.io/zh-cn/latest/part-designDocument/intro.html)

[测试文档](https://kea-technic-docs.readthedocs.io/zh-cn/latest/part-experiment/trophies.html)

### 工具安装与快速开始

**环境要求：**

- Python 3.9+
- `adb` 或 `hdc` 命令行工具可用
- 连接一个安卓或鸿蒙设备/模拟器

**工具安装：**

在终端中输入以下命令安装Kea。

```bash
git clone https://gitlab.eduxiji.net/T202410269994802/project2608128-276509.git
cd Kea
pip install -e .
```

**快速开始**

```
kea -f example.py -a omninotes.apk
```

### 工具系统测试

覆盖率报告: https://xixianliang.github.io/kea-technic-docs/

### [版本历史](https://gitlab.eduxiji.net/T202410269994802/project2608128-276509/-/tags)

**v2.0.3**
优化错误报告，修复了一些错误

**v2.0.2**
优化带状态的测试，修复了一些错误

**v2.0.1**
修改了uidumper技术，修复了一些错误

**v2.0.0**
工具重大重构，更新用户接口

**v1.3.1**
提升交互自动化能力

**v1.3.0**
新增 LLM Policy

**v1.2.0**
工具重构，新增鸿蒙设备，kea for harmonyOS

**v1.1.1**
修改了提供的mainPath样例

**v1.1.0**
新增PDL样式的mainPath定义接口

**v1.0.0**
Kea 1.0