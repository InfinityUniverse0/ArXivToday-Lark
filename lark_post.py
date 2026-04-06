"""
HTTP POST request to Lark Webhook API
"""

import json
import datetime
import requests


def post_to_lark_webhook(tag: str, papers: list, config: dict):
    headers = {
        'Content-Type': 'application/json'
    }

    # 因为飞书卡片有 100KB 容量限制，如果论文太多（比如超过10篇连带长摘要），很容易超限
    # 将长列表进行分批发送，每批最多 10 篇
    batch_size = 10
    total_batches = (len(papers) + batch_size - 1) // batch_size

    for batch_idx in range(total_batches):
        batch_papers = papers[batch_idx * batch_size : (batch_idx + 1) * batch_size]
        
        # 组装这批卡片数据
        today_date = datetime.date.today().strftime('%Y-%m-%d')
        table_rows = [
            {
                "index": i + 1 + batch_idx * batch_size,
                "title": paper['title'],
                "id": paper['id'],
                "published": paper['published'],
                "url": f"[{paper['url']}]({paper['url']})"
            }
            for i, paper in enumerate(batch_papers)
        ]
        paper_list = [
            {
                "counter": i + 1 + batch_idx * batch_size,
                "title": paper['title'],
                "id": paper['id'],
                "abstract": paper['abstract'],
                "zh_abstract": paper.get('zh_abstract', None),
                "url": paper['url'],
                "published": paper['published']
            }
            for i, paper in enumerate(batch_papers)
        ]

        card_data = {
            "type": "template",
            "data": {
                "template_id": config['template_id'],
                "template_version_name": config['template_version_name'],
                "template_variable": {
                    "today_date": f"{today_date} (Part {batch_idx + 1}/{total_batches})" if total_batches > 1 else today_date,
                    "tag": tag,
                    "total_paper": len(batch_papers),
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
        response = requests.post(config['webhook_url'], headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            print(f"Batch {batch_idx + 1}/{total_batches} - Request successful")
        else:
            print(f"Batch {batch_idx + 1}/{total_batches} - Request failed, status code: {response.status_code}")   
            print("Response:\n{}".format(response.text))

if __name__ == '__main__':
    papers = [
        {
            'title': 'Title 1',
            'id': '1234567890',
            'abstract': 'Abstract 1',
            'url': 'https://arxiv.org/abs/1234567890',
            'published': '2021-01-01',
            'zh_abstract': None
        },
        {
            'title': 'Title 2',
            'id': '2345678901',
            'abstract': 'Abstract 2',
            'url': 'https://arxiv.org/abs/2345678901',
            'published': '2021-01-02',
            'zh_abstract': '中文摘要 2'
        }
    ]
    from utils import load_config
    config = load_config()
    post_to_lark_webhook('test', papers, config)
