import streamlit as st
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team import Team
import os
from dotenv import load_dotenv
from pathlib import Path
import PyPDF2
import docx
import tempfile

# Load environment variables
load_dotenv()

# Verify API key
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_KEY:
    st.error("⚠️ Please set OPENROUTER_API_KEY in your .env file.")
    st.stop()

# Initialize model
model = OpenAIChat(
    id="mistralai/mistral-7b-instruct",
    api_key=OPENROUTER_KEY,
    base_url="https://openrouter.ai/api/v1",
)

def extract_text(file_path: Path):
    """Extract text from PDF, DOCX, or TXT files"""
    try:
        if file_path.suffix.lower() == '.pdf':
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                return "\n".join(page.extract_text() or "" for page in reader.pages)
        elif file_path.suffix.lower() == '.docx':
            doc = docx.Document(file_path)
            return "\n".join(para.text for para in doc.paragraphs)
        elif file_path.suffix.lower() == '.txt':
            return file_path.read_text(encoding="utf-8", errors="ignore")
        return "Error: Unsupported file type"
    except Exception as e:
        return f"Error processing file: {str(e)}"

def evaluate_candidate(job_desc: str, resume_text: str):
    """Evaluate candidate using specialized agents"""
    skills_agent = Agent(
        name="Skills Evaluator",
        role="Assess technical skills match",
        model=model,
        instructions="""Analyze the candidate's technical skills against job requirements.
        Response format:
        SKILLS VERDICT: EXCELLENT/GOOD/PARTIAL/POOR MATCH
        MATCHING SKILLS: [list]
        MISSING SKILLS: [list]
        SKILL GAP ANALYSIS: [detailed assessment]""",
        show_tool_calls=False
    )

    experience_agent = Agent(
        name="Experience Analyst",
        role="Evaluate professional experience",
        model=model,
        instructions="""Assess relevance and depth of work experience.
        Response format:
        EXPERIENCE VERDICT: STRONG/MODERATE/WEAK MATCH
        RELEVANT EXPERIENCE: [years, roles]
        EXPERIENCE GAPS: [missing experience]
        IMPACT ANALYSIS: [achievements assessment]""",
        show_tool_calls=False
    )

    culture_agent = Agent(
        name="Culture Fit Assessor",
        role="Evaluate cultural compatibility",
        model=model,
        instructions="""Analyze soft skills and cultural fit indicators.
        Response format:
        CULTURE VERDICT: STRONG/MODERATE/WEAK FIT
        POSITIVE INDICATORS: [evidence]
        POTENTIAL CONCERNS: [risks]
        RECOMMENDATIONS: [onboarding suggestions]""",
        show_tool_calls=False
    )

    education_agent = Agent(
        name="Education Verifier",
        role="Assess educational qualifications",
        model=model,
        instructions="""Evaluate formal education and certifications.
        Response format:
        EDUCATION VERDICT: EXCEEDS/MEETS/BELOW REQUIREMENTS
        DEGREES/CERTIFICATIONS: [list]
        RELEVANT TRAINING: [notable courses]
        KNOWLEDGE GAPS: [missing education]""",
        show_tool_calls=False
    )

    hiring_team = Team(
        mode="sequential",
        members=[skills_agent, experience_agent, culture_agent, education_agent],
        model=model,
        instructions="""Conduct comprehensive candidate evaluation in this order:
        1. Technical skills assessment
        2. Professional experience analysis
        3. Cultural fit evaluation
        4. Educational qualifications verification
        5. Decide: selected for interview or not.
        Provide final hiring recommendation with confidence score in percentage.""",
        show_tool_calls=True
    )

    evaluation_input = f"""
    JOB DESCRIPTION:
    {job_desc}

    CANDIDATE RESUME:
    {resume_text[:10000]}
    """

    return hiring_team.run(evaluation_input)

# ---------------- STREAMLIT UI ----------------
st.title("📄 AI Resume Evaluation System")
st.write("Upload a resume and job description to get an AI-powered hiring evaluation.")

job_desc = st.text_area("📝 Job Description", height=150)

uploaded_resume = st.file_uploader("📂 Upload Resume (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"])

if st.button("🚀 Evaluate Candidate"):
    if not job_desc.strip():
        st.error("Please enter a job description.")
    elif not uploaded_resume:
        st.error("Please upload a resume file.")
    else:
        with st.spinner("Processing resume..."):
            # Preserve original extension
            suffix = Path(uploaded_resume.name).suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                tmp_file.write(uploaded_resume.read())
                temp_path = Path(tmp_file.name)

            resume_text = extract_text(temp_path)

            if resume_text.startswith("Error"):
                st.error(resume_text)
            else:
                st.success("✅ Resume extracted successfully")
                st.info("🔍 Starting evaluation...")
                result = evaluate_candidate(job_desc, resume_text)

                output_text = result.content if hasattr(result, 'content') else str(result)

                # Show result in Streamlit
                st.markdown("## 📝 Evaluation Report")
                st.markdown(output_text)

                # Save to markdown file
                with open("evaluation.md", "w", encoding="utf-8") as f:
                    f.write(output_text)

                st.success("📁 Evaluation saved to `evaluation.md`")
