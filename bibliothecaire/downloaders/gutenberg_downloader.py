import logging
from pathlib import Path
from typing import List, Optional, Tuple
from urllib.parse import quote_plus

from bs4 import BeautifulSoup

from .base_downloader import BaseDownloader
from .utils import sanitize_filename, save_text_to_file

logger = logging.getLogger(__name__)


GUTENBERG_BASE_URL = "https://www.gutenberg.org"


class GutenbergDownloader(BaseDownloader):
    def download(self, author_name: str) -> None:
        author_folder = self._author_folder(author_name)
        query = quote_plus(author_name)
        search_url = f"{GUTENBERG_BASE_URL}/ebooks/search/?query={query}"

        response = self._retry_fetch(search_url)
        if not response:
            return

        soup = BeautifulSoup(response.content, "html.parser")
        book_links = self._extract_links(soup)
        if not book_links:
            logger.info(f"No books found for {author_name}")
            return

        for book_url in book_links:
            self._process_work(book_url, author_folder)

    def _extract_links(self, soup: BeautifulSoup) -> List[str]:
        return [
            GUTENBERG_BASE_URL + link['href']
            for link in soup.select("li.booklink a[href^='/ebooks/']")
        ]

    def _process_work(self, book_url: str, author_folder: Path) -> None:
        page = self._retry_fetch(book_url)
        if not page:
            logger.warning(f"Could not fetch book page: {book_url}")
            return

        soup = BeautifulSoup(page.text, "html.parser")
        title, is_french = self._extract_metadata(soup)
        if not is_french:
            logger.info(f"Skipping non-French book: {title}")
            return

        text_url = self._extract_text_link(soup)
        if not text_url:
            logger.warning(f"No text URL found for {title}")
            return

        text_response = self._retry_fetch(text_url)
        if text_response:
            file_path = author_folder / f"{sanitize_filename(title)}.txt"
            try:
                save_text_to_file(text_response.text, str(file_path))
            except Exception as e:
                logger.error(f"Failed to save file {file_path}: {e}")
            self._delay()

    @staticmethod
    def _extract_metadata(soup: BeautifulSoup) -> Tuple[str, bool]:
        metadata = soup.find('table', class_='bibrec')
        title, is_french = "Unknown_Title", False
        if metadata:
            for row in metadata.find_all('tr'):
                key = row.find('th')
                val = row.find('td')
                if not key or not val:
                    continue
                key_text = key.text.strip()
                val_text = val.text.strip()
                if key_text == "Language" and "French" in val_text:
                    is_french = True
                elif key_text == "Title":
                    title = val_text
        return title, is_french

    @staticmethod
    def _extract_text_link(soup: BeautifulSoup) -> Optional[str]:
        for link in soup.find_all('a', href=True):
            if 'txt.utf-8' in link['href']:
                return GUTENBERG_BASE_URL + link['href']
        return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    combined = GutenbergDownloader(folder_path="downloads")
    combined.download("Victor Hugo")
