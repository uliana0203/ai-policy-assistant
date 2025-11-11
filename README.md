# 🧠 AI Policy Research Assistant  
**Multi-Agent System for Automated Policy Analysis, Fact-Checking, and Report Generation**

> **UA / EN bilingual overview** — created by *Uliana Zbezhkhovska, PhD*  
> Intelligent multi-agent assistant that autonomously conducts policy research, verifies data, writes reports, and emails the results to the user.

---

## Project Overview

This project implements an **AI-powered research pipeline** combining multiple agents coordinated via `ResearchManager`.  
Each agent performs a distinct task in the research workflow — planning, searching, fact-checking, writing, and emailing.

### 🧩 Agent Architecture
| Agent | Function |
|--------|-----------|
| **PlannerAgent** | Generates 3–5 structured search queries targeting EU, OECD, UN, RAND, MIT |
| **SearchAgent** | Performs factual search via OpenAI model |
| **FactCheckerAgent** | Validates credibility and filters misinformation |
| **WriterAgent** | Produces a markdown policy brief (executive summary, challenges, recommendations) |
| **Guardrails** | Applies ethical, privacy, and structure checks |
| **EmailAgent** | Sends the final report via SendGrid |

---

## 📂 Directory Structure

```
ai-policy-assistant/
│
├── ui/
│   └── app.py                  # Gradio front-end
│
├── core/
│   └── research_manager.py     # Main async orchestration
│
├── agents/
│   ├── __init__.py             # Base Async Agent class
│   ├── planner_agent.py        # Generates search plan
│   ├── search_agent.py         # Performs factual searches
│   ├── fact_checker_agent.py   # Validates and filters results
│   ├── writer_agent.py         # Generates markdown report
│   ├── guardrails.py           # Runs quality & ethics checks
│   └── email_agent.py          # Sends results via SendGrid
│
├── requirements.txt
├── Dockerfile
├── .env
└── docker-compose.yml
```
---

## ⚙️ Local Setup

### 1️⃣ Clone the repo
```bash
git clone https://github.com/uliana0203/ai-policy-assistant.git
cd ai-policy-assistant
```

### 2️⃣ Install dependencies
```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate (Windows)
pip install -r requirements.txt
```

### 3️⃣ Create `.env`
Add your credentials:
```bash
OPENAI_API_KEY=sk-***************************
SENDGRID_API_KEY=SG.***************************
EMAIL_SENDER=your_verified_sendgrid_email@example.com
```

### 4️⃣ Run locally
```bash
python -m ui.app
```

Visit [http://127.0.0.1:7860](http://127.0.0.1:7860)

Add `share=True` to `app.launch()` for a public Gradio link.

---

## 🐳 Docker Deployment

### Build
```bash
docker build -t ai-policy-assistant .
```

### Run
```bash
docker run -p 7860:7860 --env-file .env ai-policy-assistant
```

or use Docker Compose:
```bash
docker compose up --build
```

---

## 🧠 Example Output

### Executive Summary
> The EU AI Act represents a comprehensive framework for responsible artificial intelligence regulation across member states...

### Key Policy Challenges
- Balancing innovation and compliance  
- Managing algorithmic transparency  

### Recommendations
1. Develop risk-based audit mechanisms  
2. Strengthen cross-sector coordination  
3. Encourage open standards for AI governance  

---

## 🔐 Environment Variables

| Variable | Description |
|-----------|-------------|
| `OPENAI_API_KEY` | API key for OpenAI GPT models |
| `SENDGRID_API_KEY` | API key for SendGrid email service |
| `EMAIL_SENDER` | Verified sender email address |
| `PORT` | Optional port (default: 7860) |

---

## 🧰 Technologies Used

| Component | Stack |
|------------|--------|
| **Frontend** | Gradio 4.x |
| **Backend** | Python 3.11 (asyncio) |
| **AI Engine** | OpenAI GPT-4o / GPT-4o-mini |
| **Email Delivery** | SendGrid API |
| **Containerization** | Docker |
| **Utilities** | Pydantic · dotenv · markdown |

---

## 👩‍💻 Author

**Uliana Zbezhkhovska, PhD**  
[lyasya3@gmail.com](mailto:lyasya3@gmail.com)  


