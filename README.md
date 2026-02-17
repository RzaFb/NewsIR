# NewsIR

NewsIR is a Python-based information retrieval system designed for efficient searching and ranking of news articles using advanced text processing and TF-IDF-based algorithms. The project demonstrates the core principles of information retrieval, including document indexing, term statistics computation, and query-based ranking, all tailored for a real-world news dataset.

This system enables users to preprocess a collection of news articles, build a positional index for fast term lookups, compute TF-IDF vectors for each document, and perform ranked search queries to retrieve the most relevant articles. The modular design includes utilities for adding new data, managing dictionaries and word statistics, and analyzing term distributions. NewsIR is ideal for students, researchers, and developers interested in natural language processing, search engines, or text mining, and serves as a practical foundation for building more complex IR systems.

---

## Table of Contents
- [Usage](#usage)
  - [Indexing](#indexing)
  - [Searching](#searching)
  - [Utilities](#utilities)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Testing & CI](#testing--ci)
- [Acknowledgements](#acknowledgements)

---

## Usage

### Indexing
- Build a positional index and compute TF-IDF vectors for the news dataset:
  ```bash
  python make.py
  ```

### Searching
- Search for relevant news articles using TF-IDF ranking:
  ```bash
  python use.py
  ```
- The script will prompt for a query and return the most relevant articles.

### Utilities
- Add new articles to the dataset:
  ```bash
  python add.py
  ```
- Manage dictionary and word statistics:
  ```bash
  python dict.py
  python word.py
  ```
- Compute and analyze TF-IDF and related statistics:
  ```bash
  python tfdf.py
  python tfidfd.py
  ```

---

## Features
- **Positional Indexing:** Efficient mapping of terms to their positions and frequencies in documents.
- **TF-IDF Ranking:** Computes term frequency-inverse document frequency vectors for robust search and ranking.
- **Search Engine:** Retrieves and ranks news articles based on query relevance.
- **Data Management:** Add, update, and process news articles and term statistics.
- **Extensible Utilities:** Modular scripts for dictionary, word, and index management.

---

## Installation

### Prerequisites
- Python 3.8+
- pip

### Install Dependencies
If required, add dependencies to `requirements.txt` and install:
```bash
pip install -r requirements.txt
```

---

## Quick Start

1. **Prepare Data**
   - Place your news articles in `data/news.json`.

2. **Build Index**
   ```bash
   python make.py
   ```

3. **Search**
   ```bash
   python use.py
   ```

---

## Project Structure
```
IRR/
│
├── add.py                  # Add new articles
├── dict.py                 # Dictionary management
├── main.py                 # Main entry point (optional)
├── make.py                 # Build index and TF-IDF vectors
├── tfdf.py                 # TF-DF statistics
├── tfidfd.py               # TF-IDF statistics
├── use.py                  # Search and ranking
├── word.py                 # Word processing utilities
├── data/
│   ├── news.json           # News articles dataset
│   ├── positional_index.json
│   ├── tf_idf_vectors.json
│   ├── words_sorted_by_idf.json
├── index_data/             # Additional index files
└── README.md               # This file
```

---

## Configuration
- Data files are located in the `data/` directory.
- Index and statistics files are generated automatically.
- Scripts can be extended for custom processing or integration.

---

## Testing & CI
- Run scripts individually to verify functionality.
- Add unit tests as needed for core modules.
- Integrate with CI tools for automated testing.

---

## Acknowledgements
- [Python](https://python.org/)
- Open source contributors

---

NewsIR: Efficient, scalable information retrieval for news articles using TF-IDF and advanced indexing.
