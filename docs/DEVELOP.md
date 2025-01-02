## 文档架构

#### source
放的主要是中文rst文件

#### source/conf.py
sphinx配置文件，很重要

#### source/locales
翻译文件

#### readthedocs.yaml
readthedocs托管部署文件，因为这个文件不在仓库的root，需要在readthedocs里手动配置

#### gpt_translator_utlis.py & gpt_translator.py
gpt翻译器，配置API可用。

## Build 文档

### 配置sphinx环境
```bash
cd docs
pip install -r requirements.txt
```

> 如果需要使用autodocs，还要安装Kea里的所有依赖，因为sphinx会load Kea的代码文件，缺少依赖会import报错使autodocs失效

### Build 中文文档

```bash
cd docs
make clean
make html
```

### build 英文版翻译文档
```bash
make clean
sphinx-build -b html -D language='en' source build
```

## 文档翻译

### 中文文档更新后提取翻译文件

强烈建议！先备份一份locales再执行如下操作
```bash
# 备份至 _locales
cp -r locales _locales
```

执行如下make语句，调用sphinx-intl获取新的pot内容
```bash
make clean
make gettext
```

默认输出是在 `build/gettext` ，根据实际情况执行下面的内容。

执行如下命令，sphinx-intl会将 pot 内容根据差异自动应用在现在翻译的 `.po` 文件上。
```bash
sphinx-intl update -p build/gettext
```

### 应用gpt进行自动翻译
到 [chatAnywhere](https://github.com/chatanywhere/GPT_API_free) 领个免费的 API key （一天200次4o-mini够用了应该）

把你的 API key 通过环境变量的方式存下来
```bash
export OPENAI_API_KEY="<YOUR_API>"
```

根据你的编写的内容在prompt中添加术语表，打开 `gpt_translator_utils.py` ，在 GLOSSARY 里添加。
```python
GLOSSARY = """
性质 -> property
基于性质的测试 -> property-based testing
"""
```

执行 `gpt_translator.py`，它会把所有的 `.po` 扫一遍然后翻译。