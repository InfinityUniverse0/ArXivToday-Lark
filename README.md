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

## To Do

- [ ] Use LLMs for more accurate paper filtering.

- [x] Use LLMs to translate paper abstracts.

- [ ] Predict paper impact using LLMs.

  > Zhao P, Xing Q, Dou K, et al. From Words to Worth: Newborn Article Impact Prediction with LLM[J]. arXiv preprint arXiv:2408.03934, 2024.

## Usage

### Prerequisite

1. Clone this repository.

   ```sh
   git clone https://github.com/InfinityUniverse0/ArXivToday-Lark.git
   ```

2. Create and activate aconda environment.

   ```sh
   conda create -n arxiv python=3.10
   conda activate arxiv
   ```

3. Install the required Python packages.

   ```sh
   cd ArXivToday-Lark
   pip install -r requirements.txt
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

1. Webhook URL of the Lark bot.
2. ID and version number of the Lark message card template.
3. Translation Engine Used。
4. API Key, Base URL, and Model Name of the Translation Engine.

Adjust these settings according to your specific setup.

#### Run the Script

Run the script using Python:

```sh
python main.py
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
   24 14 * * 1-5 /absolute/path/to/your/python/interpreter /absolute/path/to/ArXivToday-Lark/main.py
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

## Extension

This project can be extended to meet custom requirements. For instance:

- You can design your own message card styles or use other message types.
- You can integrate a [Lark App Bot](https://open.feishu.cn/document/client-docs/bot-v3/bot-overview) (might require additional permissions) to implement more complex workflows.

## License

This project is under the [GPL-3.0 License](LICENSE).

## Contact

For any questions, suggestions, or feedback, feel free to reach out:

- **Email**: wtxInfinity@outlook.com, lxmliu2002@126.com
- **GitHub Issues**: [Issues Page](https://github.com/InfinityUniverse0/ArXivToday-Lark/issues)

Feel free to contribute, report issues, or suggest improvements!
