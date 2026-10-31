import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"


def query_llama(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json().get("response", "No response from model.")
    except Exception as e:
        return f"Error communicating with LLaMA model: {e}"


def hr_resume_screening(resume_text, job_description):
    prompt = f"""
You are an AI HR Recruitment Assistant performing a STRICT resume screening.

Your task is to EVALUATE MATCH QUALITY using a scoring system.

==============================
SCORING RULES (TOTAL = 100)
==============================

1. Skills Match (40 points)
- Most required skills present = 35-40
- Some skills missing = 20-30
- Major skills missing = 0-15

2. Experience Relevance (30 points)
- Direct relevant experience = 25-30
- Partially relevant = 15-24
- Irrelevant or fresher = 0-14

3. Education Fit (15 points)
- Exact or strong match = 12-15
- Acceptable but not ideal = 6-11
- Not relevant = 0-5

4. Role Alignment (15 points)
- Resume clearly matches job role = 12-15
- Some alignment = 6-11
- Different career direction = 0-5

==============================

JOB DESCRIPTION:
{job_description}

CANDIDATE RESUME:
{resume_text}

==============================

INSTRUCTIONS:
1. Calculate EACH category score separately
2. Show the breakdown
3. Then give FINAL TOTAL SCORE out of 100
4. List Matching Skills
5. List Missing Skills
6. Give Hiring Recommendation (Yes / Maybe / No)
7. Suggest 3 interview questions targeting missing areas

Be strict and realistic. Do NOT give high scores unless clearly justified.
"""
    return query_llama(prompt)

