"""
Main Script
"""

import time
import datetime
import schedule
from arxiv_paper import get_latest_papers, filter_papers_by_keyword, deduplicate_papers, prepend_to_json_file
from lark_post import post_to_lark_webhook

# Paper Configuration  TODO: Change paper configuration for your own need
tag = 'LLM Security'
category_list = ['cs.CL', 'cs.CV', 'cs.AI']
keyword_list = [
    'safety', 'security', 'adversarial', 'jailbreak', 'backdoor', 'hallucination', 'victim'
]
paper_file = 'papers.json'


def task():
    """
    Main task: Fetch Papers & Post to Lark Webhook
    """
    today_date = datetime.date.today().strftime('%Y-%m-%d')
    print('Task: {}'.format(today_date))

    papers = []
    for category in category_list:
        papers.extend(get_latest_papers(category, max_results=100))
    print('Total papers: {}'.format(len(papers)))

    papers = filter_papers_by_keyword(papers, keyword_list)
    print('Filtered papers: {}'.format(len(papers)))

    papers = deduplicate_papers(papers, paper_file)
    print('Deduplicated papers: {}'.format(len(papers)))

    prepend_to_json_file(paper_file, papers)

    # Post to Lark Webhook
    post_to_lark_webhook(tag, papers)


if __name__ == '__main__':
    # Run the task immediately
    task()

    # Schedule the task to run every day at 10:17
    schedule.every().day.at("10:17").do(task)  # TODO: Change the time for your own need

    while True:
        schedule.run_pending()
        time.sleep(1)
