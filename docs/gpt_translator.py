import os
from gpt_translator_utils import OpenaiTranslator, POT_TRANSLATION_PROMPT, get_not_translated_files

if __name__ == "__main__":
    # 从环境变量中读取 API 密钥
    api_key = os.getenv("OPENAI_API_KEY")
    translater = OpenaiTranslator(api_key=api_key, prompt=POT_TRANSLATION_PROMPT)
    
    docs_dir = os.path.split(os.path.abspath(__file__))[0]
    os.chdir(docs_dir)
    
    untranslated_files = get_not_translated_files()
    
    print(f"found {len(untranslated_files)} untranslated files.")
    
    if len(untranslated_files) > 0:  
        for untranslated_file in untranslated_files:
            print(untranslated_file)
        
        print(f"===== start translating {len(untranslated_files)} files =====")
        
        for i, untranslated_file in enumerate(untranslated_files):
            print(f"({i+1}/{len(untranslated_files)}) translating {untranslated_file}")
            abs_path = os.path.join(docs_dir, untranslated_file)
            translater.translate_file(abs_path)