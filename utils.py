"""
Utility Functions
"""

import os
import yaml
from openai import OpenAI


def load_config():
    yaml_file = os.path.join(os.path.dirname(__file__), 'config.yaml')
    with open(yaml_file, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


def validate_llm_server_config(config: dict) -> dict:
    """
    Validate the configuration of LLM Server
    """
    fields = ['model', 'base_url', 'api_key']
    for field in fields:
        if field not in config:
            raise ValueError('Missing field `{}` in the configuration'.format(field))
    llm_server_config = {
        'model': config['model'],
        'base_url': config['base_url'],
        'api_key': config['api_key']
    }
    if not llm_server_config['api_key']:
        llm_server_config['api_key'] = 'ollama'  # Default for ollama service (any non-empty string)
    return llm_server_config


def get_llm_response(prompt: str, config: dict):
    """
    Get LLM response
    :param prompt: user prompt
    :param config: LLM Server configuration, fields include `model`, `base_url`, `api_key` etc.
    :return: the response content or None if failed
    """
    llm_server_config = validate_llm_server_config(config)
    model = llm_server_config['model']
    base_url = llm_server_config['base_url']
    api_key = llm_server_config['api_key']

    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    messages = [
        {
            'role': 'user',
            'content': prompt
        },
    ]
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print('LLM Server Error: {}'.format(e))
        return None


if __name__ == '__main__':
    config = load_config()
    print(config)
