import logging
from pathlib import Path
from typing import List, Tuple

from bs4 import BeautifulSoup

from .base_downloader import BaseDownloader
from .utils import sanitize_filename, save_text_to_file

logger = logging.getLogger(__name__)


WIKISOURCE_BASE_URL = "https://fr.wikisource.org"
CHARS_THRESHOLD = 1000


class WikisourceDownloader(BaseDownloader):
    def download(self, author_name: str) -> None:
        author_folder = self._author_folder(author_name)
        url = f"{WIKISOURCE_BASE_URL}/wiki/Auteur:{author_name.replace(' ', '_')}"

        response = self._retry_fetch(url)
        if not response:
            return

        soup = BeautifulSoup(response.text, "html.parser")
        work_links = self._extract_links(soup)

        for title, work_url in work_links:
            self._process_work(title, work_url, author_folder)

    def _extract_links(self, soup: BeautifulSoup) -> List[Tuple[str, str]]:
        return [
            (link.text.strip(), WIKISOURCE_BASE_URL + link['href'])
            for link in soup.select("div.mw-parser-output ul li a")
            if link.get('href', '').startswith('/wiki/')
            and "poésies" not in link.text.lower()
            and "poème" not in link.text.lower()
        ]

    def _process_work(self, title: str, url: str, author_folder: Path) -> None:
        title = sanitize_filename(title)
        if not title:
            return


        response = self._retry_fetch(url)
        if not response:
            return

        soup = BeautifulSoup(response.text, "html.parser")
        content_block = soup.find("div", class_="mw-parser-output")
        if not content_block:
            return

        paragraphs = [
            p.get_text().strip()
            for p in content_block.find_all("p")
            if p.get_text().strip()
        ]

        if not paragraphs:
            return

        text = "\n".join(paragraphs)
        if len(text) < CHARS_THRESHOLD:
            return

        file_path = author_folder / f"{title}.txt"
        save_text_to_file(text, str(file_path))
        self._delay()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    combined = WikisourceDownloader(folder_path="downloads")
    combined.download("Victor Hugo")
