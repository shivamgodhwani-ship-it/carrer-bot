import json
from job_finder import find_jobs
from scorer import score_job
from resume_tailor import tailor_resume

# LOAD PROFILE
with open("profile.json", "r") as file:
    profile = json.load(file)

# FIND JOBS
jobs = find_jobs()
print(f"\nFound {len(jobs)} jobs.\n")

# PROCESS JOBS
for job in jobs:

    print("=" * 50)
    print(f"\nProcessing: {job['title']}\n")

    score_result = score_job(profile, job["description"])
    print("\nScore Result:\n")
    print(score_result)

    try:
        parsed_score = json.loads(score_result)
        score = parsed_score.get("score", 0)

        if score >= 8:
            print("\nHigh relevance job found!\n")
            tailored_resume = tailor_resume(profile, job["description"])
            print("\nTailored Resume Output:\n")
            print(tailored_resume)
        else:
            print("\nSkipping low relevance job.\n")

    except Exception as e:
        print("Error parsing score:", e)
