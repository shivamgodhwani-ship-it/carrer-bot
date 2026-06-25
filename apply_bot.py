import os
import json
import sys
import time
from datetime import datetime

from playwright.sync_api import sync_playwright
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

PROFILE_CONTEXT = """
Name: Shivam Godhwani
College: IIM Bangalore (BBA Digital Business & Entrepreneurship) + Shyam Lal College DU (BA Economics & English)
SGPA: 8.0
Skills: Brand Strategy, GTM Execution, Analytical Thinking, Research & Synthesis, Stakeholder Coordination, Structured Communication
Experience: CII member - drove 230+ registrations, 40K+ impressions, designed 30-question business quiz
Projects:
- Himchi Cafe website (Swiggy/Zomato integration, WhatsApp reservation funnel) - GTM execution
- Rs.250 zero-budget venture at IIM Bangalore - 66% ROI, 40% profit margin using SCAMPER framework
- Pixels & Profits business growth case - Best Human Connection award at IIM Bangalore
- NFHS-5 gender and health disparities study - data analysis and visualisation
Awards: Best Human Connection at IIM Bangalore (featured on IIMB Instagram), HPAIR selectee
Interests: AI and Technology, Growth Marketing, Startups, Business Strategy, Brand Building
Location: Delhi, open to remote and hybrid
Available: Immediately
English proficiency: 5/5
"""

os.makedirs("screenshots", exist_ok=True)


def generate_answer(question, answer_type="text"):
    prompt = f"""
You are filling out an internship application for Shivam Godhwani.

CANDIDATE PROFILE:
{PROFILE_CONTEXT}

QUESTION: {question}

Instructions:
- Answer in first person, directly and confidently
- 2-4 sentences for text questions
- Use specific details from the profile where relevant
- Sound genuine, not robotic
- If yes/no: respond with just Yes or No

Return ONLY the answer, nothing else.
"""
    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"  AI error: {e}")
        return "I am highly motivated and bring strong analytical and communication skills to this role."


# Load and deduplicate jobs
with open("filtered_jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

seen = set()
unique_jobs = []
for job in jobs:
    if job["link"] not in seen:
        seen.add(job["link"])
        unique_jobs.append(job)

print(f"\n{'='*50}")
print(f"  CAREER BOT - AUTO APPLY")
print(f"  {len(unique_jobs)} unique jobs")
print(f"{'='*50}")
print("""
Before pressing Enter:
1. Run launch_chrome.bat to open Chrome with debugging
2. Log into Internshala in that Chrome window
""")
input("Press ENTER when ready...")

log = []

with sync_playwright() as p:

    try:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.new_page()
        print("\nConnected to Chrome\n")
    except Exception as e:
        print(f"\nERROR: Could not connect to Chrome.\nRun launch_chrome.bat first.\nDetail: {e}\n")
        sys.exit(1)

    applied_count = 0
    failed_count = 0

    for idx, job in enumerate(unique_jobs):

        print(f"\n[{idx+1}/{len(unique_jobs)}] {job['title']} @ {job['company']}")

        result = {
            "job": job['title'],
            "company": job['company'],
            "status": "",
            "time": datetime.now().strftime("%H:%M:%S")
        }

        try:
            page.goto(job["link"], wait_until="domcontentloaded", timeout=60000)
            time.sleep(3)

            # Close popups
            for sel in [".modal_close_icon", ".ic-24-cross",
                        "button:has-text('Maybe later')", "button:has-text('Skip')"]:
                try:
                    el = page.locator(sel).first
                    if el.is_visible(timeout=1000):
                        el.click()
                        time.sleep(0.5)
                except:
                    pass

            # Click Apply
            apply_selectors = [
                "#apply_now_button",
                ".detail_page_apply_button",
                "button#apply_now_btn",
                "button:has-text('Apply now')",
                "button:has-text('Apply Now')",
                "a:has-text('Apply now')",
                ".apply_button",
            ]

            clicked_apply = False
            for sel in apply_selectors:
                try:
                    btn = page.locator(sel).first
                    if btn.is_visible(timeout=2000):
                        btn.scroll_into_view_if_needed()
                        time.sleep(0.3)
                        btn.click()
                        clicked_apply = True
                        time.sleep(4)
                        break
                except:
                    pass

            if not clicked_apply:
                try:
                    page.evaluate("""
                        const btns = [...document.querySelectorAll('button, a')];
                        const apply = btns.find(b => b.innerText.toLowerCase().includes('apply now'));
                        if (apply) apply.click();
                    """)
                    clicked_apply = True
                    time.sleep(4)
                except:
                    pass

            if not clicked_apply:
                print(f"  SKIP: no apply button found")
                result["status"] = "failed - no apply button"
                failed_count += 1
                log.append(result)
                continue

            print("  Clicked Apply")

            # Availability radio
            for label_text in ["Yes, I am available to join immediately", "available to join immediately"]:
                try:
                    radio = page.locator(f"label:has-text('{label_text}')").first
                    if radio.is_visible(timeout=1500):
                        radio.click()
                        time.sleep(0.5)
                        break
                except:
                    pass

            time.sleep(2)

            # Fill textareas
            textareas = page.locator("textarea").all()
            for i, textarea in enumerate(textareas):
                try:
                    if not textarea.is_visible(timeout=1500):
                        continue
                    question_text = ""
                    try:
                        question_text = textarea.evaluate("""
                            (el) => {
                                let node = el.parentElement;
                                for (let i = 0; i < 6; i++) {
                                    if (!node) break;
                                    let text = (node.innerText || '').replace('Enter text ...', '').trim();
                                    if (text.length > 10) return text;
                                    node = node.parentElement;
                                }
                                return '';
                            }
                        """).strip().replace("Enter text ...", "").strip()
                    except:
                        pass
                    if not question_text:
                        question_text = "Why are you interested in this internship?"
                    print(f"  Q: {question_text[:70]}...")
                    answer = generate_answer(question_text)
                    print(f"  A: {answer[:70]}...")
                    textarea.scroll_into_view_if_needed()
                    textarea.click()
                    time.sleep(0.2)
                    textarea.fill(answer)
                    time.sleep(0.4)
                except Exception as e:
                    print(f"  textarea error: {e}")

            # Handle dropdowns
            try:
                for sel_el in page.locator("select:visible").all():
                    try:
                        options = [o.inner_text() for o in sel_el.locator("option").all()
                                   if o.inner_text().strip() and "select" not in o.inner_text().lower()]
                        if options:
                            if any(c.isdigit() for c in "".join(options)):
                                best = max(options, key=lambda x: int(''.join(filter(str.isdigit, x)) or '0'))
                                sel_el.select_option(label=best)
                            else:
                                sel_el.select_option(label=options[0])
                        time.sleep(0.3)
                    except:
                        pass
            except:
                pass

            # Handle Yes/No radios
            try:
                for block in page.locator(".additional_question, .form-group").all():
                    try:
                        block_text = block.inner_text(timeout=1000).strip()
                        yes_label = block.locator("label:has-text('Yes')").first
                        no_label = block.locator("label:has-text('No')").first
                        if yes_label.count() > 0 and no_label.count() > 0 and len(block_text) > 5:
                            ai_ans = generate_answer(block_text, "yes_no")
                            if "yes" in ai_ans.lower():
                                yes_label.click()
                            else:
                                no_label.click()
                            time.sleep(0.4)
                    except:
                        pass
            except:
                pass

            # Screenshot before submit
            safe_name = job['company'].replace(' ', '_').replace('/', '_')
            timestamp = datetime.now().strftime("%H%M%S")
            screenshot_path = f"screenshots/{timestamp}_{safe_name}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"  Screenshot: {screenshot_path}")

            # Submit
            submitted = False
            for sel in [
                "button:has-text('Submit')",
                "button:has-text('Submit application')",
                ".submit_button",
                "button.btn-primary:visible",
            ]:
                try:
                    btn = page.locator(sel).last
                    if btn.is_visible(timeout=2000):
                        btn.scroll_into_view_if_needed()
                        btn.click()
                        submitted = True
                        time.sleep(4)
                        break
                except:
                    pass

            if submitted:
                print(f"  SUBMITTED")
                result["status"] = "applied"
                applied_count += 1
            else:
                print(f"  WARNING: could not auto-submit — check screenshot")
                result["status"] = "failed - submit button not found"
                failed_count += 1

            log.append(result)
            time.sleep(2)

        except Exception as e:
            print(f"  ERROR: {e}")
            result["status"] = f"error: {e}"
            failed_count += 1
            log.append(result)

    with open("application_log.json", "w") as f:
        json.dump(log, f, indent=2)

    print(f"\n{'='*50}")
    print(f"  DONE")
    print(f"  Applied: {applied_count} | Failed: {failed_count}")
    print(f"  Log saved: application_log.json")
    print(f"  Screenshots: screenshots/")
    print(f"{'='*50}\n")
    input("Press ENTER to close...")
