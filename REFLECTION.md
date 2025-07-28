# Short Project Reflection

## 1. Overall Concept Understanding of The Project

This project automates the end-to-end process of transforming messy web content into a structured knowledge base for an AI assistant. The core components include:

- **Scraping** articles from a Zendesk-based support site via API.
- **Cleaning & converting** content into Markdown format (compatible with OpenAI’s vector store).
- **Delta detection** to identify added or updated articles using content hashing.
- **Uploading** relevant Markdown files to OpenAI via API and attaching them to a vector store.
- **Scheduling** the whole pipeline as a daily job on a DigitalOcean Droplet using Docker and `cron`.

## 2. Approach and Solution Chosen

### **Scraping:**

- Used Zendesk Help Center API to fetch articles, handling pagination with max 20 articles per page.

### **Cleaning & Markdown conversion:**

- Removed non-essential tags (`nav`, `footer`, `script`, etc.) using BeautifulSoup.
- Converted cleaned HTML to ATX-style Markdown using `markdownify`.
- File names generated with `slugify`.

### **Uploading to Vector Store:**

- Uploaded files to OpenAI File Storage, created a vector store if needed, and attached files.
- Chunking Strategy: auto

### **Delta detection (add/update/skip):**

To avoid re-uploading unchanged articles and to reduce token usage, I implemented a delta detection system based on content hashing.

- **Hashing strategy**:
  - For each article, I extracted its `title` and cleaned `HTML content`, then used SHA256 to generate a hash.
  - This hash represents the current “state” of the article.
  - Hashes are stored locally in a JSON file in the following format:
    ```json
    {
      "article-title-slug": "hash-value"
    }
    ```
- **During each run** (`main.py`):
  - All articles are re-fetched from the API (up to `MAX_ARTICLES`).
  - For each article:
    - Generate a fresh hash of its cleaned content.
    - Compare it with the previous hash stored in the JSON file.

#### Decision Logic

| Condition          | Action                                                                 |
| ------------------ | ---------------------------------------------------------------------- |
| **New article**    | `Add` => Convert to Markdown, upload to OpenAI, attach to Vector Store |
| **Hash changed**   | `Update` => Delete old file from OpenAI + re-upload and re-attach      |
| **Hash unchanged** | `Skip` => No action taken                                              |

#### Update Flow (Detailed Steps)

For `updated` articles:

- Use `slug` as the file name to locate matching files in:
  - OpenAI **File Storage**
  - **Vector Store** file list
- If found:
  - Delete both the old file and its vector store link via OpenAI API
  - Upload the new file
  - Attach it again to the Vector Store

### **Deployment:**

- Deployed the project using Docker on a DigitalOcean Droplet.
- Created a cron job for daily execution (`main.py`).

## 3. Learning New Things I Haven’t Learned before

To learn unfamiliar tools (e.g., OpenAI API, vector store management, Docker cron deployment), I followed this process:

- Skimmed official docs to understand key concepts and flow.
- Used AI assistants and documentation to clarify unclear parts.
- Built a minimal working version first to validate core flow.
- Iteratively improved structure, modularity, and error handling.
- Reflected and documented key takeaways after successful deployment.

## 4. Thoughts and Suggestions on OptiBots

OptiBot already serves as a helpful assistant for OptiSigns customers. Here are a few suggestions to enhance its usefulness:

- **Personalization:** If users are logged in, using their name in replies could make the bot feel more engaging and human.
- **UX improvements:** Add a loading indicator while waiting for responses — currently, the interface appears static during long responses.
- **Accessibility:** Consider adding text-to-speech support for users with reading difficulties.
- **Mobile readiness:** A Progressive Web App (PWA) version of OptiBot could make it more accessible on mobile devices.

## 5. Potential challenges & Solutions:

| Challenge                       | Description                                                                                                         | Suggested Solution                                                                                          |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Delayed content sync**        | If articles are updated between two scheduled reloads (e.g., daily), the assistant may return outdated information. | Use trigger-based reloads to update immediately, or schedule more frequent reloads (e.g., every 2–3 hours). |
| **Increasing embedding costs**  | As document volume grows, token and storage usage can become expensive.                                             | Optimize chunking, deduplicate uploads, and consider archiving rarely used content.                         |
| **Incorrect content retrieval** | Poor chunking logic or long articles can lead to irrelevant answers.                                                | Improve chunking granularity and attach metadata to boost relevance.                                        |
