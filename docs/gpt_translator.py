import os
from gpt_translator_utils import OpenaiTranslator, POT_TRANSLATION_PROMPT

if __name__ == "__main__":
    # 从环境变量中读取 API 密钥
    api_key = os.getenv("OPENAI_API_KEY")
    translater = OpenaiTranslator(api_key=api_key, prompt=POT_TRANSLATION_PROMPT)
    
    cur_dir = os.path.split(os.path.abspath(__file__))[0]
    locales_path = os.path.join(cur_dir, "source", "locales")
    print(f"walking dir {locales_path} for po files")
    for root, dirs, files in os.walk(locales_path):
        for file in files:
            if file.endswith('.po'):
                # 获取完整的文件路径
                file_path = os.path.join(root, file)
                print(file_path)
                translater.translate_file(file_path)