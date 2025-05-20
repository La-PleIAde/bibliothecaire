# 📚 Bibliothécaire

Le Bibliothécaire is a Python library designed to automatically download and clean French literary texts from online public domain sources such as [Project Gutenberg](https://www.gutenberg.org) and [Wikisource](https://fr.wikisource.org). It provides a unified interface for bulk downloading and standardized text cleanup — ideal for building corpora for NLP, digital humanities, or literary analysis.

---

## 🧱 Project Structure

```

le\_bibliothecaire/
├── cleaner/
│   ├── clean\_up.py            # Cleans and normalizes downloaded text
│   └── **init**.py
├── downloaders/
│   ├── base\_downloader.py     # Abstract downloader with retry & delay logic
│   ├── gutenberg\_downloader.py
│   ├── wikisource\_downloader.py
│   ├── combined\_downloader.py # Unified interface for all sources
│   ├── utils.py               # Shared helper functions
│   └── **init**.py
├── **init**.py
├── setup.py
├── LICENSE.md
└── README.md

````

---

## 🚀 Features

- ✅ Download texts by French authors from Project Gutenberg and French Wikisource.
- ✅ Unified interface for triggering downloads from all sources.
- ✅ Retry logic with exponential backoff and randomized delays to reduce server strain.
- ✅ File system-safe naming and automatic directory organization by author.
- ✅ Clean-up pipeline for:
  - Removing metadata, boilerplate headers, and footers.
  - Trimming prologues, epilogues, and chapter markers.
  - Removing non-literary markers like export notes.
- ✅ CLI support for batch cleaning text files in a directory.

---

## 🔧 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/le_bibliothecaire.git
cd le_bibliothecaire
````

Install dependencies (use a virtualenv if needed):

```bash
pip install -r requirements.txt
```

Or install as a package:

```bash
pip install .
```

---

## 📥 Downloading Texts

Use the CombinedDownloader to fetch works by an author from all supported sources:

```python
from le_bibliothecaire import CombinedDownloader

downloader = CombinedDownloader(base_folder="downloads")
downloader.download_all("Victor Hugo")
```

You can also use individual downloaders if desired:

```python
from le_bibliothecaire import GutenbergDownloader, WikisourceDownloader

gutenberg = GutenbergDownloader("downloads")
gutenberg.download("Jules Verne")

wikisource = WikisourceDownloader("downloads")
wikisource.download("Émile Zola")
```

---

## 🧽 Cleaning Texts

To clean up downloaded files:

```bash
python le_bibliothecaire/cleaner/clean_up.py downloads cleaned_texts
```

This will:

* Recursively scan the downloads/ folder
* Clean all .txt files
* Write cleaned versions to cleaned\_texts/, preserving folder structure

Alternatively, call from Python:

```python
from le_bibliothecaire.cleaner.clean_up import process_directory

process_directory("downloads", "cleaned_texts")
```

---

## 🧪 Example Output

After downloading and cleaning Victor Hugo:

```
downloads/
└── Victor Hugo/
    ├── Les Misérables.txt
    └── Notre-Dame de Paris.txt

cleaned_texts/
└── Victor Hugo/
    ├── Les Misérables.txt
    └── Notre-Dame de Paris.txt
```

---

## 🛠 Configuration

All downloaders support:

* Retries on failure (default: 3)
* Random delays between requests (default: 1–4s)
* Optional toggling of Gutenberg/Wikisource via flags

Example:

```python
CombinedDownloader(
    base_folder="downloads",
    retries=5,
    delay_range=(2, 5),
    enable_delay=True,
    gutenberg_enabled=True,
    wikisource_enabled=False,
)
```

---

## 🧱 Dependencies

* requests
* beautifulsoup4
* Python 3.8+

Install them with:

```bash
pip install requests beautifulsoup4
```

---

## 📝 License

This project is licensed under the terms of the MIT License. See the LICENSE.md file for details.

---

## 🙌 Acknowledgments

* Project Gutenberg: [https://www.gutenberg.org](https://www.gutenberg.org)
* French Wikisource: [https://fr.wikisource.org](https://fr.wikisource.org)
* Inspired by open-source scrapers and literary data initiatives.

---

## ✨ Future Ideas

* Add async download mode for faster scraping
* Support other languages (EN, DE, etc.)
* Add automatic EPUB or PDF conversion
* Integrate with HuggingFace datasets

---

📮 For questions or contributions, feel free to open an issue or pull request!
