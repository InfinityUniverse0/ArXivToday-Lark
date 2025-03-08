"""
Get arXiv papers
"""

import os
import json
import arxiv
from llms import translate_abstract


def get_latest_papers(category, max_results=100):
    """
    Get the latest papers from arXiv
    :param category: the category of papers
    :param max_results: the maximum number of papers to get
    :return: a list of papers
    """
    client = arxiv.Client()
    search_query = f'cat:{category}'
    search = arxiv.Search(
        query=search_query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    papers = []
    for result in client.results(search):
        # Remove the version number from the id
        paper_id = result.get_short_id()
        version_pos = paper_id.find('v')
        if version_pos != -1:
            paper_id = paper_id[:version_pos]

        paper = {
            'title': result.title,
            'id': paper_id,
            'abstract': result.summary.replace('\n', ' '),  # Remove line breaks
            'url': result.entry_id,
            'published': result.published.date().isoformat()  # Get the date in ISO format
        }
        papers.append(paper)

    return papers


def filter_papers_by_keyword(papers, keyword_list):
    """
    Filter papers by keywords
    :param papers: a list of papers
    :param keyword_list: a list of keywords
    :return: a list of filtered papers
    """
    results = []

    # Below is a less efficient way to filter papers by keywords
    # keyword_list = [keyword.lower() for keyword in keyword_list]
    # for paper in papers:
    #     if any(keyword in paper['abstract'].lower() for keyword in keyword_list):
    #         results.append(paper)

    keyword_set = set(keyword.lower() for keyword in keyword_list)
    for paper in papers:
        if keyword_set & set(paper['abstract'].lower().split()):
            results.append(paper)

    return results


def deduplicate_papers(papers, file_path):
    """
    Deduplicate the papers according to the previous records
    :param papers: a list of papers
    :param file_path: the file path of the previous records
    :return: the deduplicated papers
    """
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        if content:
            content = json.loads(content)
            # Filter out the duplicated papers by id
            content_id = set(d['id'] for d in content)
            papers = [d for d in papers if d['id'] not in content_id]
    if len(set(d['id'] for d in papers)) == len(papers):
        return papers
    # Deduplicate papers while maintaining the order
    # **Note**: Used in the case where multiple categories are involved
    papers_id = set()
    deduplicated_papers = []
    for paper in papers:
        if paper['id'] not in papers_id:
            papers_id.add(paper['id'])
            deduplicated_papers.append(paper)
    return deduplicated_papers

def translate_abstracts(papers, translation_service):
    """
    Translates the abstracts using the specified translation service
    :param papers: a list of papers
    :param translation_service: the translation service to use ('ollama' or 'openai')
    """
    translated_papers = []
    for paper in papers:
        abstract = paper["abstract"]
        paper["zh_abstract"] = None
        if translation_service != None:
            zh_abstract = translate_abstract(abstract, translation_service)
            paper["zh_abstract"] = zh_abstract
        translated_papers.append(paper)
        # break
    return translated_papers


def prepend_to_json_file(file_path, data):
    """
    Prepend data to a JSON file
    :param file_path: the file path
    :param data: the data to prepend
    """
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        if content:
            content = json.loads(content)
        else:
            content = []
    else:
        content = []

    with open(file_path, 'w') as f:
        json.dump(data + content, f, indent=4)




if __name__ == '__main__':
    papers = get_latest_papers('cs.CL', max_results=50)
    print(json.dumps(papers, indent=4))
    print()
    keyword_list = ['safety', 'security', 'adversarial', 'jailbreak', 'backdoor', 'hallucination', 'victim']
    results = filter_papers_by_keyword(papers, keyword_list)
    print(json.dumps(results, indent=4))
    print()
    results = deduplicate_papers(results, 'papers.json')
    print(json.dumps(results, indent=4))
    print()
    prepend_to_json_file('papers.json', results)
