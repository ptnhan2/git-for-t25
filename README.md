# Optibot Article Scraper & Vector Uploader

This project scrapes help articles from OptiSigns support site, converts them to clean Markdown, and uploads them to OpenAI's vector store for use with a custom Assistant chatbot.

---

## Setup (local)

1. Create a `.env` file (similar to .env.sample)
2. Fill in your actual values in .env (especially OPENAI_API_KEY).
3. Install dependencies: pip install -r requirements.txt
4. Run the scraper + uploader:

## Run with Docker

1. Build the Docker image: docker build -t optibot .

2. Run the script: docker run -e OPENAI_API_KEY=... optibot

## Daily job logs

The scraper & uploader job is deployed on a **DigitalOcean Platform (Droplet)**.  
It is scheduled using a standard **cron job** inside the Linux environment

To validate delta detection logic (added/updated/skipped), I temporarily scheduled the job to run **every 2 minutes** using the following cron syntax:

```cron
*/2 * * * * docker run --rm -e OPENAI_API_KEY=$OPENAI_API_KEY optibot
```

For production usage, the job can be scheduled to run once per day at 7:00 AM:

```cron
0 7 * * * docker run --rm -e OPENAI_API_KEY=$OPENAI_API_KEY optibot
```

Test cases:

- **First run: Add 30 new articles** => detected as `Added: 0, Updated: 0, Skipped: 30`
- **Updated 1 article** by modifying its hash => correctly detected as `Added: 0, Updated: 0, Skipped: 301`.
- **Added 1 new article and update 1 article** => detected as `Added: 1, Updated: 1, Skipped: 28`.

Logs available here: https://github.com/ptnhan2/git-for-t25/blob/dev/logs/job.log

## Screenshot

![Playground Screenshot](https://github.com/ptnhan2/git-for-t25/blob/dev/assets/ScreenAssistants.png)
