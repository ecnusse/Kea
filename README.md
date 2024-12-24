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

保障移动应用质量是移动操作系统生态建设的关键。现有业界普遍采用的移动应用测试与分析技术（如人工/脚本测试、静态分析技术、界面测试技术）存在人力成本高、检错能力弱、功能场景无感知的局限性，很难用于自动化检测移动应用的功能测试中。因此，如何实现移动应用的自动化功能测试一直是一个具有挑战性的问题。

基于性质测试理论（Property-Based Testing，PBT）于2000年在函数式编程领域提出。该理论方法以被测系统应满足的性质为测试断言， 通过自动生成大量随机输入数据以验证这些性质是否在各种情况下保持正确。 与传统测试相比，基于性质的测试能够高效有效地覆盖被测系统输入空间及其边界情况，从而发现深层次的功能缺陷。

Kea是**首个**基于性质测试理论设计开发的移动应用自动化功能测试工具。目前支持鸿蒙(OpenHarmony/HarmonyOS)和安卓应用软件的自动化功能测试。Kea设计了：(1)一套面向移动应用的性质描述语言（可支持用户编写以前置条件、交互场景、后置条件为主要形式的应用功能性质），(2)三种页面探索策略：随机遍历、基于主路径遍历、大模型引导的路径遍历（自动生成事件序列来达到应用更深层的状态，有效覆盖移动应用事件探索空间）。

### 工具文档

[工具文档](https://kea-technic-docs.readthedocs.io/zh-cn/latest/part-theory/introduction.html)

[用户手册](https://kea-technic-docs.readthedocs.io/zh-cn/latest/part-keaUserManuel/envirnment_setup.html)

[设计文档](https://kea-technic-docs.readthedocs.io/zh-cn/latest/part-designDocument/intro.html)

[测试文档](https://kea-technic-docs.readthedocs.io/zh-cn/latest/part-experiment/trophies.html)

### 工具安装与快速开始

**环境要求：**

- Python 3.9+
- `adb` 或 `hdc` 命令行工具可用
- 连接一个安卓或鸿蒙设备/模拟器

安卓及鸿蒙环境配置可参考 [环境配置教程](https://kea-technic-docs.readthedocs.io/zh-cn/latest/part-keaUserManuel/envirnment_setup.html)

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