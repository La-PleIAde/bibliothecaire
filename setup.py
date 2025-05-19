from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="bibliothecaire",
    version="0.1.0",
    description="Download and clean French public domain literature from Project Gutenberg and Wikisource.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="La PléIAde",
    author_email="muradmustafayev03@gmail.com",
    url="https://github.com/La-PleIAde/le_bibliothecaire",
    project_urls={
        "Source": "https://github.com/La-PleIAde/le_bibliothecaire",
        "Tracker": "https://github.com/La-PleIAde/le_bibliothecaire/issues",
    },
    license="MIT",
    packages=find_packages(exclude=["tests", "examples", "downloads"]),
    python_requires=">=3.8",
    install_requires=[
        "requests",
        "beautifulsoup4"
    ],
    entry_points={
        'console_scripts': [
            'process_file = bibliothecaire:process_file',
            'process_directory = bibliothecaire:process_directory',
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Natural Language :: English",
        "Natural Language :: French",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: EducationTopic :: Education",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    keywords="gutenberg wikisource nlp text-processing french corpus literature",
    include_package_data=True,
    zip_safe=False,
)
