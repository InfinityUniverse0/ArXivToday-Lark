import yaml
import requests
import openai
import re
from openai import OpenAI

def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

def translate_with_ollama(abstract, config):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "model": config["ollama"]["model"],
        "prompt": f"请将下面的文章摘要翻译成中文。\n{abstract}\n注意，请直接给出翻译结果，不需要其他任何内容。",
        "format": "json",
        "stream": False
    }
    response = requests.post(f'{config["ollama"]["base_url"]}/api/generate', json=data, headers=headers)
    
    if response.status_code == 200:
        try:
            result = response.json()
            translated_text = result.get('response', '')
            pattern = r'\"(.*?)\"'
            matches = re.findall(pattern, translated_text, re.DOTALL)
            cleaned_text = ''.join(matches).strip().replace('\n', '').replace('  ', ' ')
            return cleaned_text
        except Exception as e:
            return "翻译引擎错误"
    else:
        return "翻译引擎错误"

def translate_with_openai(abstract, config):
    api_key = config["openai"]["api_key"]
    base_url = config["openai"]["base_url"]
    model = config["openai"]["model"]

    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一名专业的学术论文翻译助手。"},
                {"role": "user", "content": f"请将下面的文章摘要翻译成中文。\n{abstract}\n注意，请直接给出翻译结果，不需要其他任何内容。"}
            ]
        )
        return completion.choices[0].message.content

    except openai.error.OpenAIError as e:
        return "翻译引擎错误"

    except Exception as e:
        return "翻译引擎错误"


def translate_abstract(abstract:str, translation_service):
    config = load_config()
    abstract = abstract.replace('\n', '')
    if translation_service == 'ollama':
        return translate_with_ollama(abstract, config)
    elif translation_service == 'openai':
        return translate_with_openai(abstract, config)
    else:
        raise ValueError("Unsupported translation service")