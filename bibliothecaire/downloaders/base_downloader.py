import logging
import random
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Tuple

from requests import Response

from .utils import sanitize_filename, fetch_page

logger = logging.getLogger(__name__)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
]


class BaseDownloader(ABC):
    def __init__(self, folder_path: str, retries: int = 3, delay_range: Tuple[int, int] = (1, 4), enable_delay: bool = True):
        """
        Initialize a downloader with retry logic and optional delay between requests.
        """
        self.folder_path = Path(folder_path)
        self.retries = retries
        self.delay_range = delay_range
        self.enable_delay = enable_delay

    @staticmethod
    def _random_headers() -> dict:
        return {"User-Agent": random.choice(USER_AGENTS)}

    def _retry_fetch(self, url: str) -> Optional[Response]:
        for attempt in range(1, self.retries + 1):
            logger.info(f"Fetching: {url} (attempt {attempt}/{self.retries})")
            try:
                response = fetch_page(url, headers=self._random_headers())
                if response:
                    return response
            except Exception as e:
                logger.warning(f"Fetch failed for {url}: {e}")
            sleep_time = min(2 ** attempt + random.random(), 10)
            logger.warning(f"Retry {attempt} failed. Sleeping {sleep_time:.2f}s...")
            time.sleep(sleep_time)
        logger.error(f"Failed after {self.retries} attempts: {url}")
        return None

    def _author_folder(self, author: str) -> Path:
        folder = self.folder_path / sanitize_filename(author)
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    def _delay(self) -> None:
        if self.enable_delay:
            time.sleep(random.uniform(*self.delay_range))

    @abstractmethod
    def download(self, author_name: str) -> None:
        pass

    @abstractmethod
    def _extract_links(self, soup) -> list:
        pass

    @abstractmethod
    def _process_work(self, *args, **kwargs) -> None:
        pass
