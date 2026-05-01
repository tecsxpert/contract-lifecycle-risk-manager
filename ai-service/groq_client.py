import logging
import os
import time
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise SystemExit("Set GROQ_API_KEY in .env before running this script.")

DEFAULT_GROQ_API_URL = os.getenv("GROQ_API_URL", "https://api.groq.com/v1/models")


class GroqClient:
    def __init__(self, base_url: str | None = None, api_key: str | None = None, timeout: int = 10, max_retries: int = 3):
        self.base_url = base_url or DEFAULT_GROQ_API_URL
        self.api_key = api_key or GROQ_API_KEY
        self.timeout = timeout
        self.max_retries = max_retries
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def fetch_models(self) -> Any:
        return self._get(self.base_url)

    def _get(self, url: str) -> Any:
        backoff = 1
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info("GroqClient request attempt %s to %s", attempt, url)
                response = requests.get(url, headers=self.headers, timeout=self.timeout)
                if response.status_code >= 500 or response.status_code == 429:
                    logger.warning("Received retryable HTTP status %s", response.status_code)
                    raise requests.exceptions.HTTPError(
                        f"HTTP {response.status_code} error", response=response
                    )
                response.raise_for_status()
                try:
                    return response.json()
                except ValueError as parse_error:
                    logger.error("Failed to parse JSON from Groq response: %s", parse_error)
                    raise
            except requests.exceptions.RequestException as error:
                logger.error("Groq request failed on attempt %s: %s", attempt, error)
                if attempt == self.max_retries:
                    logger.error("Max retries reached for Groq request")
                    raise
                logger.info("Sleeping %s seconds before retry", backoff)
                time.sleep(backoff)
                backoff *= 2
        raise RuntimeError("Groq request failed after retries")
