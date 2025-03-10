"""
Use LLM for Translation
"""

import re
from tqdm import tqdm
from utils import load_config, get_llm_response


def translate_abstract(abstract: str, config: dict):
    """
    Translate the abstract using LLM
    :param abstract: the abstract to translate
    :param config: the configuration of LLM Server
    :return: the translated abstract or None if failed
    """
    prompt = '请将下面的学术论文摘要翻译为中文：\n{}\n\n**注意**：\n- 中文语境中常用的英文学术术语可以保留英文原文，如：自然语言处理中的 Transformer 可以保留英文。\n- 其他关键的学术术语可以中英文对照，如：后门攻击(Backdoor Attack)。\n- 直接给出翻译结果，不需要进行解释，不需要任何其他内容。'.format(abstract)
    translated_text = get_llm_response(prompt, config)
    if not translated_text:
        return None
    # Filter out the thinking process wrapped between <think> and </think> (if any)
    translated_text = re.sub(r'<think>.*?</think>', '', translated_text, flags=re.DOTALL)
    return translated_text.strip()


def translate_abstracts(papers: list):
    """
    Translate the abstracts using the specified translation service
    :param papers: a list of papers
    :return: the translated papers
    """
    config = load_config()
    for paper in tqdm(papers, desc='Translating Abstracts'):
        abstract = paper["abstract"]
        zh_abstract = translate_abstract(abstract, config)
        paper["zh_abstract"] = None
        if zh_abstract:
            paper["zh_abstract"] = zh_abstract
    return papers
