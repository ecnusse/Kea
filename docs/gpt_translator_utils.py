from openai import OpenAI
import os
import logging
import re
import subprocess
class OpenaiTranslator:
    def __init__(self, api_key:str, prompt):
        self.logger = logging.getLogger(name=self.__class__.__name__)
        # 创建 OpenAI 客户端实例
        self.client = OpenAI(
            api_key=api_key,
            base_url=r"https://api.chatanywhere.tech"
        )
        self.prompt = prompt


    def translate_text(self, text):
        # 使用流式传输请求翻译文本
        stream = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "system",
                "content": self.prompt
                },   
                {"role": "user", 
                 "content": f"{text}"}],
            stream=True,
        )
        
        translated_text = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                translated_text += chunk.choices[0].delta.content
        
        return translated_text.strip()

    def translate_file(self, file_path):
        self.logger.info(f"translating file {os.path.split(file_path)[-1]}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 翻译文本
        translated_text = self.translate_text(content)
        
        lines = translated_text.splitlines()
        begin_flag = False
        
        self.logger.info(f"writing file {os.path.split(file_path)[-1]}")
        # 输出翻译结果
        with open(file_path, "w") as fp:
            for line in lines:
                if line.strip() == "```":
                    begin_flag = True
                    continue
                if begin_flag:
                    if line.strip == "```":
                        break
                    fp.write(line+"\n")
    
    
def get_not_translated_files():
    pattern = re.compile(r".*(\d+)\s*untranslated.*")
    translation_state = subprocess.check_output(["sphinx-intl", "stat"], text=True)

    not_translated_files = []
    for line in translation_state.splitlines():
        r = re.search(pattern, line)
        unstanslated_sentences = int(r.group(1))
        file_path = line.split(":")[0]
        if unstanslated_sentences > 0:
            not_translated_files.append(file_path)
    return not_translated_files


GLOSSARY = """
性质 -> property
基于性质的测试 -> property-based testing
"""

POT_TRANSLATION_PROMPT = f"""
You are a translator, you need to translate some docs from Chinese into English using .po files.
Your input (a .po file) will be given like this:

```
# SOME DESCRIPTIVE TITLE.
# Copyright (C) 2024, ECNU-SE-lab
# This file is distributed under the same license as the Kea package.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: Kea 1.0\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: 2024-12-31 16:33+0800\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"

#: ../../source/index.rst:4
msgid "概述"
msgstr "Introduction"

#: ../../source/index.rst:10
#: ../../source/index.rst:12
msgid "用户手册"
msgstr ""                         
```

You need to follow these rules while translation:
1. Output the system info straightly. Don't modify them. Here is a system info example:
```
"POT-Creation-Date: 2024-12-31 16:33+0800\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
```
2. If the msgstr is not NULL, it has already been translated. Don't modify them. Output them straightly.
Here is a not NULL (already translated) example.
```
#: ../../source/index.rst:4
msgid "概述"
msgstr "Introduction"
```

3. Your translation should be enclosed in three backticks (```). Just output them directly with not explanation.

Here's the glossary for you:
{GLOSSARY}

Based on the above rules. Here's an output example for the above input.
```
# SOME DESCRIPTIVE TITLE.
# Copyright (C) 2024, ECNU-SE-lab
# This file is distributed under the same license as the Kea package.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: Kea 1.0\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: 2024-12-31 16:33+0800\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"

#: ../../source/index.rst:4
msgid "概述"
msgstr "Introduction"

#: ../../source/index.rst:10
#: ../../source/index.rst:12
msgid "用户手册"
msgstr "User Manual"
```                       
"""