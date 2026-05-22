# scraper/scrape.py
import httpx
from pydantic import BaseModel
from datetime import date
import json, time, pathlib

class JobPosting(BaseModel):
    title: str
    company: str
    location: str
    description: str
    tags: list[str]
    scraped_date: str

def scrape_jobs(query: str = "machine-learning", pages: int = 1) -> list[JobPosting]:
    jobs = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    url = f"https://remoteok.com/api?tag={query}"
    print(f"Fetching: {url}")

    try:
        r = httpx.get(url, headers=headers, timeout=15, follow_redirects=True)
        print(f"Status code: {r.status_code}")
        print(f"Response preview: {r.text[:300]}")

        data = r.json()
        print(f"Total items in response: {len(data)}")

        # First item is always metadata, skip it
        job_items = [item for item in data[1:] if isinstance(item, dict)]
        print(f"Job items found: {len(job_items)}")

        for item in job_items:
            title = item.get("position", "").strip()
            company = item.get("company", "").strip()
            description = item.get("description", "").strip()

            if not title or not company:
                continue

            jobs.append(JobPosting(
                title=title,
                company=company,
                location=item.get("location", "Worldwide"),
                description=description or title,  # fallback to title if empty
                tags=item.get("tags", []) or [],
                scraped_date=str(date.today())
            ))

    except Exception as e:
        print(f"Error fetching jobs: {e}")

    print(f"Successfully parsed {len(jobs)} jobs")

    # Save
    out = pathlib.Path(f"data/jobs_{date.today()}.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps([j.dict() for j in jobs], indent=2))
    print(f"Saved to {out}")

    return jobs