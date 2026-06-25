import json
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# LOAD JOBS
with open("jobs.json", "r") as file:
    jobs = json.load(file)

scored_jobs = []

for job in jobs:

    prompt = f"""
    You are an internship relevance scorer.

    Score this internship from 1-10 for this candidate:

    Candidate Profile:
    - BBA student
    - Interested in growth marketing
    - startup strategy
    - operations
    - analytics
    - business development
    - GTM
    - AI/startups

    Internship:
    Title: {job['title']}
    Company: {job['company']}
    Location: {job['location']}

    Return ONLY a number from 1-10.
    """

    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        score_text = response.choices[0].message.content.strip()

        try:
            score = int(score_text)
        except:
            score = 0

        job["score"] = score
        print(f"{job['title']} → {score}/10")

        if score >= 8:
            scored_jobs.append(job)

    except Exception as e:
        print("Error:", e)

# SAVE FILTERED JOBS
with open("filtered_jobs.json", "w") as file:
    json.dump(scored_jobs, file, indent=4)

print("\nSaved filtered jobs.")
