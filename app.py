import streamlit as st
from chatbot import hr_resume_screening
from pypdf import PdfReader
from openpyxl import Workbook, load_workbook
from datetime import datetime
import os

st.set_page_config(page_title="HR Resume Screening Agent", layout="wide")

st.title("🤖 HR Resume Screening Agent")
st.markdown("AI-powered resume evaluation using LLaMA 3")

EXCEL_FILE = "uploaded_resumes.xlsx"


# ----------- PDF TEXT EXTRACTION -----------
@st.cache_data(show_spinner=False)
def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text


# ----------- SAVE FILENAME TO EXCEL -----------
def save_resume_log(filename):
    if not os.path.exists(EXCEL_FILE):
        wb = Workbook()
        ws = wb.active
        ws.title = "Resume Logs"
        ws.append(["File Name", "Upload Time"])
        wb.save(EXCEL_FILE)

    wb = load_workbook(EXCEL_FILE)
    ws = wb.active
    ws.append([filename, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    wb.save(EXCEL_FILE)


# ----------- JOB DESCRIPTION INPUT -----------
st.subheader("📄 Job Description")
job_description = st.text_area("Paste the job description here", height=200)

# ----------- RESUME UPLOAD -----------
st.subheader("📎 Upload Candidate Resume (PDF)")
uploaded_file = st.file_uploader("Upload resume in PDF format", type=["pdf"])

resume_text = ""

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    save_resume_log(uploaded_file.name)  # Store filename in Excel
    st.success(f"Resume '{uploaded_file.name}' uploaded and logged successfully ✅")

# ----------- ANALYZE BUTTON -----------
if st.button("🔍 Analyze Resume"):
    if job_description and resume_text:
        with st.spinner("Analyzing candidate fit..."):
            result = hr_resume_screening(resume_text, job_description)

        st.subheader("📊 Screening Result")
        st.write(result)
    else:
        st.warning("Please provide both job description and resume PDF.")
