"""
HTTP POST request to Lark Webhook API
"""

import json
import datetime
import requests
from config import CONFIG


def post_to_lark_webhook(tag, papers):
    headers = {
        'Content-Type': 'application/json'
    }

    # Card Template Data
    today_date = datetime.date.today().strftime('%Y-%m-%d')
    table_rows = [
        {
            "index": i + 1,
            "title": paper['title'],
            "id": paper['id'],
            "published": paper['published'],
            "url": f"[{paper['url']}]({paper['url']})"
        }
        for i, paper in enumerate(papers)
    ]
    paper_list = [
        {
            "counter": i + 1,
            "title": paper['title'],
            "id": paper['id'],
            "abstract": paper['abstract'],
            "url": paper['url'],
            "published": paper['published']
        }
        for i, paper in enumerate(papers)
    ]

    card_data = {
        "type": "template",
        "data": {
            "template_id": CONFIG['template_id'],
            "template_version_name": CONFIG['template_version_name'],
            "template_variable": {
                "today_date": today_date,
                "tag": tag,
                "total_paper": len(papers),
                "table_rows": table_rows,
                "paper_list": paper_list
            }
        }
    }

    data = {
        "msg_type": "interactive",
        "card": card_data
    }

    # Send HTTP POST request
    response = requests.post(CONFIG['webhook_url'], headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("Request successful")
        print("Response:\n{}".format(response.json()))
    else:
        print("Request failed, status code: {}".format(response.status_code))
        print("Response:\n{}".format(response.text))


if __name__ == '__main__':
    papers = [
        {
            'title': 'Title 1',
            'id': '1234567890',
            'abstract': 'Abstract 1',
            'url': 'https://arxiv.org/abs/1234567890',
            'published': '2021-01-01'
        },
        {
            'title': 'Title 2',
            'id': '2345678901',
            'abstract': 'Abstract 2',
            'url': 'https://arxiv.org/abs/2345678901',
            'published': '2021-01-02'
        }
    ]
    post_to_lark_webhook('test', [])
