import json
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# LOAD PROFILE
with open("profile.json", "r") as file:
    profile = json.load(file)

# LOAD FILTERED JOBS
with open("filtered_jobs.json", "r") as file:
    jobs = json.load(file)

for job in jobs:

    print(f"\nTailoring resume for: {job['title']}")

    job_description = f"""
    Title: {job['title']}
    Company: {job['company']}
    Location: {job['location']}
    """

    prompt = f"""
    You are an expert ATS resume optimizer.

    Using the candidate profile and internship description:

    1. Tailor resume bullet points
    2. Improve wording
    3. Add ATS-friendly keywords
    4. Highlight relevant experiences
    5. Keep resume strong for this specific role

    Return valid JSON ONLY.

    Format:

    {{
        "optimized_skills": [],
        "tailored_experience": [],
        "tailored_projects": [],
        "ats_keywords": []
    }}

    Candidate Profile:
    {json.dumps(profile)}

    Internship Description:
    {job_description}
    """

    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content
        result = result.replace("```json", "").replace("```", "")
        parsed = json.loads(result)

        filename = f"tailored_{job['company'].replace(' ', '_')}.json"
        with open(filename, "w") as outfile:
            json.dump(parsed, outfile, indent=4)

        print(f"Saved: {filename}")

    except Exception as e:
        print("Error:", e)

print("\nAll resumes tailored.")
