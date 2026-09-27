# 🔬 ResearchMind: Multi-Stage AI Research Pipeline

An automated, multi-stage AI research assistant that conducts real-time web research, scrapes authoritative sources, synthesizes comprehensive reports, and subjects them to an automated critical review.

Built with **LangChain**, **Google Gemini (Gemini 2.5 Flash)**, **Tavily Search API**, and **Streamlit**.

---

## 📌 Problem It Solves

Conducting deep research on complex topics typically involves hours of manual searching, filtering through low-quality or blocked web pages, aggregating information from multiple sources, and writing structured summaries.

Standard LLM interactions also face key challenges:
- **Knowledge Cutoffs & Hallucinations**: Generic models lack access to real-time, ground-truth web information.
- **Surface-Level Content**: Search snippet results alone do not provide the depth found within the full text of articles.
- **Unverified Outputs**: Generated content often lacks self-critique and objective quality evaluations.

**ResearchMind** solves this by automating a 4-stage research workflow that retrieves live web sources, filters low-quality data, performs deep text extraction, generates structured markdown reports, and runs automated rubric evaluations.

---

## 🏗 Architecture & Workflow

ResearchMind is designed as a **multi-stage AI research pipeline**. Rather than relying on uncoordinated independent agents, it combines autonomous tool-augmented agents for data acquisition with structured LangChain Expression Language (LCEL) chains for deterministic synthesis and evaluation.

```
                               ┌───────────────────────────┐
                               │     User Research Topic   │
                               └─────────────┬─────────────┘
                                             │
                                             ▼
                       ┌───────────────────────────────────────────┐
                       │  STAGE 1: Search Agent (Tavily Search)    │
                       │  - Discovers top live web URLs & snippets │
                       └─────────────────────┬─────────────────────┘
                                             │
                                             ▼
                       ┌───────────────────────────────────────────┐
                       │  STAGE 2: Reader / Scrape Agent (BS4)     │
                       │  - Scrapes & cleans full webpage content  │
                       │  - Filters Cloudflare/captchas & low-qual │
                       └─────────────────────┬─────────────────────┘
                                             │
                                             ▼
                       ┌───────────────────────────────────────────┐
                       │  STAGE 3: Writer Chain (Gemini 2.5 Flash) │
                       │  - Synthesizes findings into full report  │
                       │  - Formats Intro, Findings, & Sources     │
                       └─────────────────────┬─────────────────────┘
                                             │
                                             ▼
                       ┌───────────────────────────────────────────┐
                       │  STAGE 4: Critic Chain (Gemini 2.5 Flash) │
                       │  - Evaluates clarity, facts, and structure│
                       │  - Outputs score (X/10), pros, and verdict│
                       └─────────────────────┬─────────────────────┘
                                             │
                                             ▼
                               ┌───────────────────────────┐
                               │ Final Report + Score Card │
                               └───────────────────────────┘
```

---

## 🔄 The 4-Stage Pipeline Breakdown

### 1. 🔍 Search Stage (Search Agent)
- Utilizes the **Tavily Search API** tailored for LLM applications.
- Queries the web in real-time to return top ranked URLs, article titles, and context snippets relevant to the prompt.

### 2. 📄 Scrape / Reader Stage (Scrape Agent & Filtering Engine)
- Fetches target HTML pages using custom headers and extracts sanitized body text via **BeautifulSoup4**.
- Removes non-content elements (`<script>`, `<style>`, `<nav>`, `<footer>`).
- Implements defensive filtering to discard:
  - Bot protection & Cloudflare challenge pages (`access denied`, `captcha`, `cloudflare`).
  - Multimedia/video boilerplate platforms (`youtube.com`, `youtu.be`).
  - Pages with low substantive content (< 500 characters).

### 3. ✍️ Writer Stage (Writer Chain)
- An LCEL prompt-to-model chain running on **Google Gemini 2.5 Flash**.
- Ingests both search summaries and scraped deep content.
- Generates a research report formatted in Markdown with:
  - **Introduction**: Context and problem framing.
  - **Key Findings**: Minimum 3 thoroughly explained core insights.
  - **Conclusion**: Forward-looking summary and implications.
  - **Sources**: Transparent list of all referenced URLs.

### 4. 🧐 Critic Stage (Critic Chain)
- An independent evaluation chain that audits the drafted report against quality and factual completeness standards.
- Produces a structured scorecard:
  - **Score**: Quantitative rating (X/10).
  - **Strengths**: Specific, bulleted positive attributes of the report.
  - **Areas to Improve**: Constructive critique for depth and omissions.
  - **One-line Verdict**: Summary assessment.

---

## ✨ Features

- **End-to-End Automation**: Runs the entire research lifecycle from a single topic query.
- **Dual Execution Modes**:
  - **Streamlit Web UI**: Interactive dashboard with pipeline status cards, real-time step progress, expandable raw outputs, and one-click report download.
  - **CLI Pipeline**: Lightweight terminal runner with Rich formatting for headless environments or quick testing.
- **Automated Anti-Scrape & Quality Filters**: Skips bot-blocked or thin pages to prevent garbage-in, garbage-out results.
- **Self-Critique & Scoring**: Automatically evaluates output quality before delivering to the user.
- **Export Ready**: Download research reports directly as standard `.md` files.

---

## 🛠 Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Core language runtime |
| **LLM Provider** | Google Gemini | `gemini-2.5-flash` model for reasoning, synthesis, and critique |
| **Orchestration** | LangChain / LangChain Core | Agent builders and LCEL prompt-model-output pipelines |
| **Search Engine** | Tavily Search API | Optimized search API designed for AI research agents |
| **Web Scraping** | BeautifulSoup4 / Requests | HTML parsing, text stripping, and page extraction |
| **User Interface** | Streamlit | Web application and dynamic step-by-step progress UI |
| **Terminal Formatting** | Rich | Enhanced console outputs for CLI mode |
| **Configuration** | python-dotenv | Secure environment variable handling |


---

## 📂 Project Structure

```
AI-Research-System/
├── app.py                # Streamlit web application & interactive UI
├── agents.py             # Agent definitions & LCEL chains (Writer & Critic)
├── pipeline.py           # CLI runner & robust content-scraping pipeline logic
├── tools.py              # Custom LangChain tools (Tavily search & BeautifulSoup scraper)
├── requirements.txt      # Project Python dependencies
├── .env.example          # Template for required environment variables
├── .gitignore            # Git exclusion rules
└── README.md             # Project documentation
```

---

## 🚀 Setup Instructions

### 1. Prerequisites
- Python 3.10 or higher
- [Google AI Studio API Key](https://aistudio.google.com/) for Gemini models
- [Tavily API Key](https://tavily.com/) for intelligent web search

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/AI-Research-System.git
cd AI-Research-System
```

### 3. Create and Activate a Virtual Environment
```bash
# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows (Command Prompt)
python -m venv .venv
.venv\Scripts\activate.bat
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 Required Environment Variables

Create a `.env` file in the root directory by copying `.env.example`:
```bash
cp .env.example .env
```

Set your API keys inside `.env`:
```env
GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

| Variable | Description | Source |
| :--- | :--- | :--- |
| `GOOGLE_API_KEY` | API key for Google Gemini model inference | [Google AI Studio](https://aistudio.google.com/) |
| `TAVILY_API_KEY` | API key for Tavily search queries | [Tavily Search](https://tavily.com/) |

---

## 🖥 How to Run

### Option 1: Streamlit Web UI (Recommended)
Run the web application:
```bash
streamlit run app.py
```
Then open `http://localhost:8501` in your browser. Enter your research topic and click **Run Research Pipeline**.

### Option 2: Command Line (CLI Pipeline)
Run the standalone terminal pipeline:
```bash
python pipeline.py
```
Enter a research topic when prompted. Step progress and formatted results will stream directly to the terminal.

---

## 📸 Screenshots

### Streamlit Web Dashboard
<img width="1920" height="4423" alt="Screenshot" src="https://github.com/user-attachments/assets/6cb764f9-e249-46ed-a665-526adce12cf9" />

---

## ⚠️ Limitations & Future Improvements

- **Asynchronous Scraping**: Currently processes URLs sequentially; adding `aiohttp` parallel requests will accelerate multi-source extraction.
- **Context Truncation**: High-volume web pages are sliced to prevent context overflow; recursive chunking/summarization can preserve more deep context.
- **Dynamic Multi-Query Search**: Expanding user queries into multiple search angles for more comprehensive subject coverage.
- **Multi-Format Export**: Supporting direct export to PDF and DOCX formats.

