from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="le_bibliothecaire",
    version="0.1.0",
    description="Download and clean French public domain literature from Project Gutenberg and Wikisource.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="you@example.com",
    url="https://github.com/yourusername/le_bibliothecaire",
    project_urls={
        "Source": "https://github.com/yourusername/le_bibliothecaire",
        "Tracker": "https://github.com/yourusername/le_bibliothecaire/issues",
    },
    license="MIT",
    packages=find_packages(exclude=["tests", "examples"]),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.0"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="gutenberg wikisource nlp text-processing french corpus literature",
    include_package_data=True,
    zip_safe=False,
)
