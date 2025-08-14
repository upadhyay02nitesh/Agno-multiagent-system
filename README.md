# 🤖 AI-Powered Resume Evaluation Tool

An AI-based resume evaluation system built with **Streamlit**, **OpenRouter (OpenAI-compatible)**, and a **multi-agent orchestration** using `agno` framework.  
It evaluates a candidate's resume against a given job description, producing a **structured hiring report** in Markdown format.

---

## 📌 Features
- 📂 **Upload Resumes** in PDF, DOCX, or TXT formats
- 📝 **Paste Job Descriptions**
- 🤝 **Multi-Agent Workflow**:
  - Skills Evaluator
  - Experience Analyst
  - Culture Fit Assessor
  - Education Verifier
- 📊 **Final Hiring Recommendation** with confidence score
- 💾 **Export Evaluation Report** as `evaluation.md`

---

## 🛠 Tech Stack
- **Python 3.10+**
- **Streamlit** – interactive UI
- **agno.agent** / **agno.team** – agent orchestration
- **OpenAIChat (via OpenRouter API)** – LLM-powered analysis
- **PyPDF2** – extract text from PDF resumes
- **python-docx** – extract text from DOCX resumes
- **dotenv** – secure API key handling

---

## 📂 Project Structure
├── app.py # Streamlit app
├── evaluation.md # Generated AI evaluation output
├── requirements.txt # Python dependencies
├── .env # API key storage (not committed)
└── README.md # Project documentation

## 🔑 Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/ai-resume-evaluator.git
cd ai-resume-evaluator

SKILLS VERDICT: GOOD MATCH
MATCHING SKILLS: Python, Flask, REST APIs
MISSING SKILLS: AWS, Kubernetes
SKILL GAP ANALYSIS: Candidate demonstrates strong backend expertise but lacks cloud deployment experience.

EXPERIENCE VERDICT: STRONG MATCH
RELEVANT EXPERIENCE: 4 years in backend development
EXPERIENCE GAPS: Limited DevOps exposure

FINAL RECOMMENDATION: Selected for interview
CONFIDENCE: 82%
