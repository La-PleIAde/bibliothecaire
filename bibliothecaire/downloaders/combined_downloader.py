import logging
from typing import Tuple

from .gutenberg_downloader import GutenbergDownloader
from .wikisource_downloader import WikisourceDownloader

logger = logging.getLogger(__name__)


class CombinedDownloader:
    def __init__(
        self,
        base_folder: str,
        retries: int = 3,
        delay_range: Tuple[int, int] = (1, 4),
        enable_delay: bool = True,
        gutenberg_enabled: bool = True,
        wikisource_enabled: bool = True,
    ):
        """
        Initializes the downloader with configuration for each source.

        Args:
            base_folder (str): Root folder to save downloaded files.
            retries (int): Number of retry attempts for network requests.
            delay_range (tuple): Min and max seconds for random delay.
            enable_delay (bool): Whether to enable delay between requests.
            gutenberg_enabled (bool): Enable or disable Gutenberg download.
            wikisource_enabled (bool): Enable or disable Wikisource download.
        """
        self.base_folder = base_folder
        self.retries = retries
        self.delay_range = delay_range
        self.enable_delay = enable_delay
        self.gutenberg_enabled = gutenberg_enabled
        self.wikisource_enabled = wikisource_enabled

        self.gutenberg = GutenbergDownloader(
            folder_path=base_folder,
            retries=retries,
            delay_range=delay_range,
            enable_delay=enable_delay,
        )
        self.wikisource = WikisourceDownloader(
            folder_path=base_folder,
            retries=retries,
            delay_range=delay_range,
            enable_delay=enable_delay,
        )

    def download_all(self, author_name: str) -> None:
        """
        Download works by the given author from all enabled sources.
        """
        logger.info(f"Starting combined download for author: {author_name}")

        if self.gutenberg_enabled:
            logger.info("Downloading from Project Gutenberg...")
            try:
                self.gutenberg.download(author_name)
            except Exception as e:
                logger.error(f"Error downloading from Gutenberg: {e}")

        if self.wikisource_enabled:
            logger.info("Downloading from Wikisource...")
            try:
                self.wikisource.download(author_name)
            except Exception as e:
                logger.error(f"Error downloading from Wikisource: {e}")

        logger.info(f"Completed combined download for author: {author_name}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    combined = CombinedDownloader(base_folder="downloads")
    combined.download_all("Victor Hugo")
