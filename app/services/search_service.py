import os
import httpx
from datetime import datetime, timezone
from dotenv import load_dotenv
from app.models.search import SearchResult, SearchResponse

load_dotenv()


class SearchService:
    SERPAPI_URL = "https://serpapi.com/search"

    def __init__(self):
        self.api_key = os.getenv("SERPAPI_API_KEY")
        self.fallback_mode = False
        self.last_error = None
        
        self.use_real_api = bool(
            self.api_key and 
            self.api_key != "TADY_VLOZ_SVUJ_SERPAPI_KEY"
        )
        
        if not self.use_real_api:
            print("SerpAPI klíč není nastaven. Používám mock data.")

    def search(self, search_query: str) -> SearchResponse:
        raw_json = self._fetch_from_serpapi(search_query)
        search_results = self._parse_organic_results(raw_json)

        provider_name = "serpapi"
        if not self.use_real_api:
            provider_name = "mock"
        elif self.fallback_mode:
            provider_name = "serpapi-fallback"

        search_response = SearchResponse(
            query=search_query,
            fetched_at=datetime.now(timezone.utc),
            provider=provider_name,
            total_returned=len(search_results),
            results=search_results,
            warning=self.last_error
        )

        return search_response

    def _fetch_from_serpapi(self, search_query: str) -> dict:
        if self.use_real_api:
            try:
                return self._call_serpapi(search_query)
            except httpx.HTTPStatusError as e:
                self.fallback_mode = True
                if e.response.status_code == 401:
                    self.last_error = "Neplatný API klíč. Zkontrolujte prosím nastavení."
                elif e.response.status_code == 402:
                    self.last_error = "Limit vyhledávání pro tento měsíc byl vyčerpán."
                elif e.response.status_code == 429:
                    self.last_error = "Příliš mnoho požadavků. Zkuste to prosím za chvíli."
                else:
                    self.last_error = f"Externí API vrátilo chybu {e.response.status_code}. Zobrazuji ukázková data."
                return self._get_mock_data()
            except httpx.TimeoutException:
                self.fallback_mode = True
                self.last_error = "Vyhledávací služba neodpověděla včas (Timeout). Zobrazuji ukázková data."
                return self._get_mock_data()
            except httpx.RequestError:
                self.fallback_mode = True
                self.last_error = "Problém s připojením k síti. Zobrazuji ukázková data."
                return self._get_mock_data()
        else:
            return self._get_mock_data()

    def _call_serpapi(self, search_query: str) -> dict:
        params = {
            "api_key": self.api_key,
            "engine": "google",
            "q": search_query,
            "num": 10,
            "hl": "cs",
            "gl": "cz"
        }
        
        with httpx.Client(timeout=10.0) as client:
            response = client.get(self.SERPAPI_URL, params=params)
            response.raise_for_status()
            return response.json()

    def _get_mock_data(self) -> dict:
        raw_json = {
            "organic_results": [
                {
                    "position": 1,
                    "title": "Python Tutorial - Official Documentation",
                    "link": "https://docs.python.org/3/tutorial/",
                    "snippet": "The Python Tutorial — Python 3.11.0 documentation. Python is an easy to learn, powerful programming language."
                },
                {
                    "position": 2,
                    "title": "Learn Python - Free Interactive Python Tutorial",
                    "link": "https://www.learnpython.org/",
                    "snippet": "Welcome to the LearnPython.org interactive Python tutorial. Whether you are an experienced programmer or not..."
                },
                {
                    "position": 3,
                    "title": "Python For Beginners",
                    "link": "https://www.python.org/about/gettingstarted/",
                    "snippet": "Getting Started with Python. New to programming? Python is free and easy to learn if you know where to start!"
                },
                {
                    "position": 4,
                    "title": "W3Schools Python Tutorial",
                    "link": "https://www.w3schools.com/python/",
                    "snippet": "Well organized and easy to understand Web building tutorials with lots of examples of how to use Python."
                },
                {
                    "position": 5,
                    "title": "Real Python Tutorials",
                    "link": "https://realpython.com/",
                    "snippet": "Learn Python online: Python tutorials for developers of all skill levels, Python books and courses, Python news..."
                }
            ]
        }
        return raw_json

    def _parse_organic_results(self, raw_json: dict) -> list[SearchResult]:
        search_results = []
        items = raw_json.get("organic_results", [])
        
        for position, item in enumerate(items, start=1):
            search_result = SearchResult(
                position=position,
                title=item.get("title", ""),
                url=item.get("link", ""),
                snippet=item.get("snippet")
            )
            search_results.append(search_result)
        
        return search_results
