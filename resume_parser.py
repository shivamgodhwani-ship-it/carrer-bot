import os
import fitz
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def parse_resume(resume_text):
    prompt = f"""
Extract important information from this resume.

Return ONLY valid JSON.

Format:
{{
  "name": "",
  "college": "",
  "skills": [],
  "experience": [],
  "projects": [],
  "interests": []
}}

Resume:
{resume_text}
"""
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    resume_text = extract_text_from_pdf("resume.pdf")
    parsed = parse_resume(resume_text)
    print(parsed)
