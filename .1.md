# 🤖 Multi-Agent AI Research System

An AI-powered multi-agent research system built with **Python, CrewAI, Gradio, Groq LLM, and Plotly**. Specialized agents collaborate to research a topic, analyze findings, and deliver a structured report with interactive visualizations, all from a simple web UI.

---

## 📌 Overview

Manual research means searching, reading, summarizing, and structuring information by hand. This project automates that workflow with a **crew of cooperating AI agents**, each with a clear role, goal, and task. Give it a topic, and the crew returns a researched, organized output you can read and explore interactively.

## ✨ Features

- **Multi-agent architecture**: role-based agents orchestrated with CrewAI
- **Automated research workflow**: from topic input to final report with no manual steps
- **Fast LLM inference**: powered by the Groq API
- **Interactive UI**: clean Gradio interface for entering topics and viewing results
- **Visualizations**: Plotly charts for exploring the output
- **Modular code**: separate entry points for the web app and the CLI

## 🧠 How It Works

```
User Topic
    │
    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  Researcher   │ →  │   Analyst     │ →  │    Writer     │
│ gathers info  │    │ extracts key  │    │ compiles the  │
│               │    │ insights      │    │ final report  │
└───────────────┘    └───────────────┘    └───────────────┘
                                                │
                                                ▼
                                   Report + Plotly Visualizations
                                          (Gradio UI)
```

> Agent names and roles above are illustrative. Update them to match the agents defined in `main.py`.

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Agent framework | CrewAI |
| LLM provider | Groq API |
| Web interface | Gradio |
| Visualization | Plotly |
| Version control | Git / GitHub |

## 📁 Project Structure

```
multi-agent-ai-research-system/
├── app.py            # Gradio web interface
├── main.py           # Agent, task, and crew definitions
├── requirements.txt  # Python dependencies
├── .env              # API keys (not committed)
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- A free [Groq API key](https://console.groq.com/)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/zananyagupta25-afk/multi-agent-ai-research-system.git
cd multi-agent-ai-research-system

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Run

**Web app (Gradio):**

```bash
python app.py
```

Then open the local URL shown in the terminal (usually `http://127.0.0.1:7860`).

**Command line:**

```bash
python main.py
```

## 💡 Usage

1. Launch the app with `python app.py`.
2. Enter a research topic, e.g. *"Impact of generative AI on healthcare"*.
3. Click **Run** and let the agents collaborate.
4. Read the generated report and explore the visualizations.

## 🖼️ Screenshots

<!-- Add screenshots here: -->
<!-- ![App UI](assets/ui.png) -->

## 🗺️ Roadmap

- [ ] Add web search / scraping tools for live data
- [ ] Export reports to PDF and Markdown
- [ ] Add memory so agents can build on earlier research
- [ ] Support multiple LLM providers
- [ ] Deploy on Hugging Face Spaces

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to open an issue or submit a pull request.

## 👩‍💻 Author

**Ananya Gupta**
B.Tech, Artificial Intelligence & Machine Learning

- GitHub: [@zananyagupta25-afk](https://github.com/zananyagupta25-afk)
- LinkedIn: [Ananya Gupta](https://www.linkedin.com/in/ananya-gupta-8b7023369)

---

⭐ If you found this project useful, consider giving it a star!
