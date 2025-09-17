# ArXiv Today

<p align="center">
    <a href="README.md">
        <img src="https://img.shields.io/badge/README-English-blue" alt="README">
    </a>
    <a href="README-zh.md">
        <img src="https://img.shields.io/badge/README-%E4%B8%AD%E6%96%87-red" alt="README-zh">
    </a>
    <img src="https://img.shields.io/badge/License-GPL--3.0-yellow" alt="License">
</p>

> ArXiv Today: Get arXiv daily papers right in your Lark (飞书) via bot.

**ArXivToday-Lark** is a lightweight tool that automates the process of fetching the latest papers from [arXiv](https://arxiv.org) and delivers them directly to your [Lark](https://www.feishu.cn) group chats using a custom bot. Designed for research enthusiasts and academic professionals, this project simplifies daily paper discovery with customizable features, seamless integration, and extendable functionality.

Key highlights include automated scheduling, support for LLM-based paper filtering, summary translation, and influence prediction (in development). Whether you’re exploring cutting-edge research or curating papers for your team, **ArXivToday-Lark** makes it easy and efficient to stay updated.

## Demo

![Demo](images/demo.png)

![Demo-Dark](images/demo-dark.png)

## Features

- [x] **Automated Paper Fetching**: Retrieve latest papers from multiple arXiv categories
- [x] **LLM-Based Paper Filtering**: Intelligently filter papers using AI models based on custom research interests
- [x] **Abstract Translation**: Automatically translate English abstracts to Chinese using LLMs
- [x] **Keyword Filtering**: Filter papers by predefined keywords for better relevance
- [x] **Lark Integration**: Send formatted message cards to Lark group chats
- [x] **Flexible Scheduling**: Support both crontab and Python schedule library for automation
- [x] **OpenAI SDK Compatible**: Works with Ollama, OpenAI, and other compatible LLM services
- [x] **Duplicate Detection**: Automatic deduplication across categories and previous runs

## To Do

- [ ] Predict paper impact using LLMs.

  > Zhao P, Xing Q, Dou K, et al. From Words to Worth: Newborn Article Impact Prediction with LLM[J]. arXiv preprint arXiv:2408.03934, 2024.

## Usage

### Prerequisite

1. Clone this repository.

   ```sh
   git clone https://github.com/InfinityUniverse0/ArXivToday-Lark.git
   ```

2. Create and activate conda environment.

   ```sh
   conda create -n arxiv
   conda activate arxiv
   ```

3. Install the required Python packages.

   ```sh
   cd ArXivToday-Lark
   pip install -r requirements.txt
   ```

## Project Structure

```
ArXivToday-Lark/
├── main.py                 # Main script entry point
├── config.yaml            # Configuration file  
├── paper_to_hunt.md       # LLM filtering prompt template
├── requirements.txt       # Python dependencies
├── ArXivToday.card        # Lark message card template
├── arxiv_paper.py         # ArXiv paper fetching and filtering
├── lark_post.py           # Lark webhook posting functionality
├── llm.py                 # LLM integration utilities
├── utils.py               # Configuration and utility functions
└── images/                # Demo screenshots
    ├── demo.png
    └── demo-dark.png
```

### Deployment

In [Lark](https://www.feishu.cn), add a **[Custom Bot](https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot)** to a group chat. Deploy and run this project to fetch the latest relevant papers from arXiv daily and push them to the group via the bot.

#### Add a Lark Custom Bot

Follow the steps in [this guide](https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot) to add a custom bot to your group chat in Lark.

#### Set Up Lark Message Card Templates

Refer to [this guide](https://open.feishu.cn/document/uAjLw4CM/ukzMukzMukzM/feishu-cards/quick-start/send-message-cards-with-custom-bot) for detailed steps on setting up message card templates in Lark.

The message card template used in the [Demo](#Demo) can be directly imported from `ArXivToday.card` and applied in Lark.

#### Configure Script Parameters

In `config.yaml`, modify the following parameters based on the results of the previous steps:

**Basic Configuration:**
1. **Webhook URL** of the Lark bot
2. **Template ID and version** of the Lark message card template  
3. **Tag** for categorizing your papers in the message card

**Paper Filtering Configuration:**
4. **ArXiv Categories** - List of arXiv categories to search (e.g., `cs.CL`, `cs.AI`, `cs.LG`)
5. **Keywords** - List of keywords for basic filtering
6. **LLM Filtering** - Enable/disable AI-based paper filtering with custom research interests

**LLM Service Configuration (Support Ollama and OpenAI SDK-compatible models):**
7. **Model Name** - e.g., `qwen2.5:7b`, `gpt-4o-mini`
8. **Base URL** - API endpoint (for Ollama: `http://localhost:11434/v1`)  
9. **API Key** - Authentication key (for Ollama: any non-empty string)

**Advanced Options:**
10. **Translation** - Enable/disable automatic abstract translation to Chinese

#### Example Configuration

```yaml
# Lark Bot Configuration
webhook_url: 'https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK'
template_id: 'YOUR_TEMPLATE_ID'
template_version_name: '1.0.0'

# Paper Configuration  
tag: 'AI Security Research'
category_list:
  - cs.CL  # Computation and Language
  - cs.AI  # Artificial Intelligence  
  - cs.CR  # Cryptography and Security
  - cs.LG  # Machine Learning

keyword_list:
  - security
  - safety
  - adversarial
  - alignment

# LLM Configuration (Ollama Example)
model: 'qwen2.5:7b'
base_url: 'http://localhost:11434/v1' 
api_key: 'ollama'
use_llm_for_filtering: true
use_llm_for_translation: true
```

For LLM-based filtering, customize the research interests in `paper_to_hunt.md` to describe what papers you're looking for.

Adjust these settings according to your specific setup.

#### Run the Script

The script will:
1. Fetch papers from configured arXiv categories
2. Filter by keywords (if configured)
3. Apply LLM-based filtering (if enabled)  
4. Translate abstracts to Chinese (if enabled)
5. Remove duplicates from previous runs
6. Send formatted cards to your Lark group

Run the script using Python:

```sh
python main.py
```

**Output Example:**
```
Task: 2024-03-10
Total papers: 387
Deduplicated papers across categories: 275
Filtered papers by Keyword: 45
Filtered papers by LLM: 12
Deduplicated papers: 9
Translated Abstracts into Chinese
Request successful
```

To run the script periodically, you can use the `crontab` command in Linux or the `schedule` library.

##### Run Periodically with crontab

> Requires a Linux system

For example, to fetch arXiv papers and push them via the Lark bot at 12:24 PM every weekday, follow these steps:

1. Open the `crontab` editor with the following command:

   ```sh
   crontab -e
   ```

2. Add the following line and save it:

   ```sh
   24 12 * * 1-5 /absolute/path/to/your/python/interpreter /absolute/path/to/ArXivToday-Lark/main.py
   ```

> [!NOTE]
>
> ⚠️ Ensure to provide **absolute paths** for both the Python interpreter and the script.

3. Verify the crontab task setup with this command:

   ```sh
   crontab -l
   ```

##### Run Periodically with the schedule Library

1. Install the dependency:

   ```sh
   pip install schedule
   ```

2. Uncomment the following section in `main.py` and modify it as needed:

    ```python
    ### Uncomment the following code to use `schedule` to run the task periodically ###
    import time
    import schedule
    # Schedule the task to run every day at 10:17
    schedule.every().day.at("10:17").do(task)  # TODO: Change the time for your own need
    while True:
        schedule.run_pending()
        time.sleep(1)
    ```

## Troubleshooting

### Common Issues

**LLM Service Connection Issues:**
- Ensure your LLM service (Ollama/OpenAI) is running and accessible
- Check the `base_url` configuration matches your service endpoint
- For Ollama, make sure to append `/v1` to the host URL

**No Papers Found:**  
- Verify your arXiv categories in `category_list` are valid
- Check if your keyword filtering is too restrictive
- Review your LLM filtering prompt in `paper_to_hunt.md`

**Lark Bot Not Responding:**
- Confirm your webhook URL is correct and active
- Ensure the message card template ID and version are properly configured
- Check if the bot has permissions to post in your group

**Permission Errors:**
- Use absolute paths in crontab configurations
- Ensure the Python interpreter and script paths are correct

### Debug Mode

To debug issues, you can run individual components:

```bash
# Test configuration loading
python -c "from utils import load_config; print(load_config())"

# Test paper fetching (without LLM)
python -c "from arxiv_paper import get_latest_papers; papers = get_latest_papers('cs.AI', 5); print(f'Found {len(papers)} papers')"

# Test LLM connection  
python -c "from utils import get_llm_response, load_config; config = load_config(); print(get_llm_response('Hello', config))"
```

## Extension

This project can be extended to meet custom requirements. For instance:

- You can design your own message card styles or use other message types.
- You can integrate a [Lark App Bot](https://open.feishu.cn/document/client-docs/bot-v3/bot-overview) (might require additional permissions) to implement more complex workflows.

## License

This project is under the [GPL-3.0 License](LICENSE).

## Contact

For any questions, suggestions, or feedback, feel free to reach out:

- **Email**: wtxInfinity@outlook.com
- **GitHub Issues**: [Issues Page](https://github.com/InfinityUniverse0/ArXivToday-Lark/issues)

Feel free to contribute, report issues, or suggest improvements!

## Contributors

- [@InfinityUniverse0](https://github.com/InfinityUniverse0)
    - **E-mail**: [wtxInfinity@outlook.com](mailto:wtxInfinity@outlook.com)
- [@lxmliu2002](https://github.com/lxmliu2002)
    - **E-mail**: [lxmliu2002@126.com](mailto:lxmliu2002@126.com)

<a href="https://github.com/InfinityUniverse0/ArXivToday-Lark/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=InfinityUniverse0/ArXivToday-Lark"/>
</a>
