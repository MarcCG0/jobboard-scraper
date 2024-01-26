from typing import Any, List

import requests
from bs4 import BeautifulSoup

from src.logs import LOGGER
from src.models.jobopportunity.models import JobOpportunity
from src.scrapers.scraper import BaseScraper


class LinkedInScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            "https://www.linkedin.com/jobs/search/?keywords={}&location={}&position=1&pageNum={}"
        )

    def scrape(self, **kwargs: Any) -> List[JobOpportunity]:
        """Given the desired settings for a job offer,
        scrapes linkedin for the specified jobs
        """
        if "keywords" not in kwargs:
            raise ValueError(
                "Missing required argument: 'keywords' that stands for the information you want to scrape."
            )
        if "location" not in kwargs:
            raise ValueError(
                "Missing required argument: 'location' that stands for place you want to scrape the positions from."
            )

        keywords = kwargs.get("keywords")
        location = kwargs.get("location")
        jobs: List[JobOpportunity] = []
        number = 0
        while True and number < 20:
            url = self.base_url.format(keywords, location, number)
            response = requests.get(url)

            soup = BeautifulSoup(response.text, "html.parser")
            job_listings = soup.find_all("div", class_="base-card")

            if not job_listings:  # Whenever we cannot find more jobs stop scraping.
                break
            LOGGER.info(f"Scraping page {number} from linkedin")
            for job in job_listings:
                title = (
                    job.find("span", class_="sr-only").text.strip()
                    if job.find("span", class_="sr-only")
                    else "No Title Found"
                )
                location_found = job.find(
                    "span", class_="job-search-card__location"
                ).text.strip()
                company = (
                    job.find("a", class_="hidden-nested-link").text.strip()
                    if job.find("a", class_="hidden-nested-link")
                    else "No Company Found"
                )
                post_time = (
                    job.find("time", class_="job-search-card__listdate").text.strip()
                    if job.find("time", class_="job-search-card__listdate")
                    else "Age not found"
                )
                url_linkedin_employer = (
                    job.find("a", class_="hidden-nested-link").get("href")
                    if job.find("a", class_="hidden-nested-link")
                    else "No employer found"
                )
                url_linkedin_offer = (
                    job.find(
                        "a",
                        class_="base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]",
                    ).get("href")
                    if job.find(
                        "a",
                        class_="base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]",
                    )
                    else "No offer link found"
                )
                jobs.append(
                    JobOpportunity(
                        job_title=title,
                        company=company,
                        location=location_found,
                        url_employer=url_linkedin_employer,
                        url_offer=url_linkedin_offer,
                        age=post_time,
                    )
                )
            # Repeat the process while we still have more pages to check
            number += 1
        return jobs


# TESTING
# scraper = LinkedInScraper().scrape(keywords = "Software Engineer", location = "Barcelona")
# print(scraper)
