from datetime import datetime, timezone
from typing import Any, List

import requests

from src.logs import LOGGER
from src.models.jobopportunity.models import JobOpportunity
from src.scrapers.scraper import BaseScraper


class InfoJobsScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://www.infojobs.net/webapp/offers/search")

    def scrape(self, **kwargs: Any) -> List[JobOpportunity]:
        """Given the desired settings for a job offer,
        scrapes infojobs for the specified jobs
        Note: in this case keywords and location are concatenated
        since the API call needed a mapping for ProvinceID and in this way
        we avoid to compute ourselves this mapping.
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
        assert type(keywords) == str
        assert type(location) == str

        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        }
        query = keywords + " " + location
        querystring = {
            "keyword": query,
            "provinceIds": "",
            "segmentId": "",
            "page": "1",
            "sortBy": "RELEVANCE",
            "onlyForeignCountry": "false",
            "sinceDate": "ANY",
        }
        jobs: List[JobOpportunity] = []
        number = 1

        while True:
            LOGGER.info(f"Scraping page {number} from infojobs")
            querystring["page"] = str(number)
            response = requests.request(
                "GET", self.base_url, headers=headers, params=querystring
            )
            offers = response.json()["offers"]

            if len(offers) == 0:
                break

            for offer in offers:
                title = offer["title"]
                company = offer["companyName"]
                location_found = offer["city"]
                url_infojobs_employer = offer["companyLink"]
                url_infojobs_offer = offer["link"]
                post_time = self.treat_age(offer["publishedAt"])
                jobs.append(
                    JobOpportunity(
                        job_title=title,
                        company=company,
                        location=location_found,
                        url_employer=url_infojobs_employer,
                        url_offer=url_infojobs_offer,
                        age=post_time,
                    )
                )
            number += 1
        return jobs

    def treat_age(self, published_at: str) -> str:
        """Given a datetime in isoformat, computes the
        needed transformations in order to compute the time
        it has passed since the publication of the job offer"""

        time_publication: datetime = datetime.fromisoformat(
            published_at.replace("Z", "+00:00")
        )
        current_time = datetime.now(timezone.utc)

        time_diff = current_time - time_publication

        days = time_diff.days
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        if days > 0:
            time_ago = f"Publicado hace {days} días"
        elif hours > 0:
            time_ago = f"Publicado hace {hours} horas"
        elif minutes > 0:
            time_ago = f"Publicado hace {minutes} minutos"
        else:
            time_ago = "Publicado recientemente"

        return time_ago


# TESTING
# print(InfoJobsScraper().scrape(keywords = "software", location = "barcelona"))
