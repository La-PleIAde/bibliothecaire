import re
import logging
from pathlib import Path
from typing import Optional
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Constants
INVALID_FILENAME_CHARS = r'[\\/*?:"<>|]'


def sanitize_filename(filename: str) -> str:
    """
    Sanitize the input string to create a safe filename.
    Replaces spaces with underscores and removes invalid characters.
    """
    cleaned = re.sub(INVALID_FILENAME_CHARS, "", "_".join(filename.split())).strip()
    return cleaned


def fetch_page(url: str, headers: Optional[dict] = None) -> Optional[requests.Response]:
    """
    Fetch a web page with optional HTTP headers.
    Returns the response object if successful, else None.
    """
    try:
        response = requests.get(url, headers=headers or {})
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logging.error(f"Failed to fetch {url}: {e}")
        return None


def save_text_to_file(text: str, path: str) -> None:
    """
    Save a given text string to a file at the specified path.
    """
    try:
        file_path = Path(path)
        file_path.write_text(text, encoding="utf-8")
        logging.info(f"Saved: {file_path}")
    except IOError as e:
        logging.error(f"Error saving file {path}: {e}")
