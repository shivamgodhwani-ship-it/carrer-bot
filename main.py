import os
import time

print("\n==============================")
print("STEP 1 — FINDING INTERNSHIPS")
print("==============================\n")

os.system("python job_finder.py")

time.sleep(2)

print("\n==============================")
print("STEP 2 — SCORING INTERNSHIPS")
print("==============================\n")

os.system("python scorer.py")

time.sleep(2)

print("\n==============================")
print("STEP 3 — TAILORING RESUMES")
print("==============================\n")

os.system("python resume_tailor.py")

time.sleep(2)

print("\n==============================")
print("STEP 4 — APPLYING")
print("==============================\n")

os.system("python apply_bot.py")

print("\n==============================")
print("ALL TASKS FINISHED")
print("==============================\n")