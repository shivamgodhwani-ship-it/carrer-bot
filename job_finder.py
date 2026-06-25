from playwright.sync_api import sync_playwright
import json
import time

locations = [
    "remote",
    "noida",
    "gurgaon",
    "delhi-ncr"
]

all_jobs = []

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    for location in locations:

        print(f"\nSearching jobs in: {location}")
        url = f"https://internshala.com/internships/{location}-internship/"
        page.goto(url)
        time.sleep(5)

        # Close popup
        try:
            page.keyboard.press("Escape")
            time.sleep(1)
        except:
            pass

        try:
            page.locator(".modal_close_icon").click(timeout=3000)
        except:
            pass

        time.sleep(3)

        cards = page.locator(".individual_internship")
        count = cards.count()
        print(f"Found {count} jobs")

        for i in range(min(count, 10)):
            try:
                card = cards.nth(i)
                title = card.locator("a.job-title-href").inner_text(timeout=5000)
                company = card.locator(".company-name").inner_text(timeout=5000)
                link = card.locator("a.job-title-href").get_attribute("href")
                full_link = "https://internshala.com" + link

                job = {
                    "title": title,
                    "company": company,
                    "location": location,
                    "link": full_link
                }

                all_jobs.append(job)
                print(job)

            except Exception as e:
                print("Skipped one card")

    with open("jobs.json", "w") as file:
        json.dump(all_jobs, file, indent=4)

    print("\nSaved jobs to jobs.json")
    browser.close()
