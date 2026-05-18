import httpx
from bs4 import BeautifulSoup
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

def scrape_jobs(query= "MLOps", pages: int=3) -> list[JobPosting]:
    jobs = []
    headers = {
        "User-Agent": "Mozilla/5.0"}
    
    for page in range(pages):
        # using RemoteOK as an example (has a public JSON API)
        url = f"https://remoteok.com/api?tag={query}"

        r = httpx.get(url, headers=headers, timeout=10)
        data = r.json()[1:] #first item is metadata

        for item in data:
            jobs.append(JobPosting(
                title=item.get("position", ""),
                company=item.get("company", ""),
                location=item.get("location", "Worldwide"),
                description=item.get("description", ""),
                tags=item.get("tags", []),
                scraped_date=str(date.today())
            ))

        time.sleep(2)

    #save raw data
    out = pathlib.Path(f"data/jobs_{date.today()}.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps([j.dict() for j in jobs], indent=2))

    return jobs
 