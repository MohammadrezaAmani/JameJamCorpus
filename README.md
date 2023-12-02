By [Mohammadreza Amani](https://github.com/MohammadrezaAmani) and [Mobina Afshari](https://github.com/Mobina-Afshari/) for [AbrLabs](https://github.com/AbrLabs). ☁️🌖


<p align="center">
    <a>
        <img src="./assets/images/jamejam.svg" alt="dataset_image" width="640">
    </a>
    <br>
    <b>A universe of information within your fingertips. </b>
    <br>
    <a href="https://example.com">
        Download
    </a>
    •
    <a href="https://example.com">
        Documentation
    </a>
    •
    <a href="https://t.me/AbrLabs">
        Channel
    </a>
    •
    <a href="mailto:more.amani@yahoo.com">
        Support
    </a>
</p>

<br>

# Jam-e Jam News Corpus

Welcome to the official repository for the Jam-e Jam News Dataset and NLP Model. This repository contains a comprehensive dataset of news articles scraped from the [Jam-e Jam Online](https://jamejamonline.ir) website. The dataset includes information such as title, tags, types, timestamp, summary, and content for over 1.4 million news articles.

In addition to the dataset, we have developed a powerful NLP model for classifying news articles based on their types and tags. This model can be used for tasks such as text classification.

## <a name='Contents'></a>Contents
<!-- vscode-markdown-toc -->
- [Jam-e Jam News Corpus](#jam-e-jam-news-corpus)
  - [Contents](#contents)
  - [Dataset Formats](#dataset-formats)
  - [NLP Model](#nlp-model)
  - [Requirements](#requirements)
    - [**Python Compatibility**](#python-compatibility)
    - [**Dependencies**](#dependencies)
  - [Instructions](#instructions)
    - [Scrap data](#scrap-data)
      - [Clone the Repository](#clone-the-repository)
      - [Create and Activate Virtual Environment](#create-and-activate-virtual-environment)
      - [Install Requirements](#install-requirements)
    - [How to Work](#how-to-work)
    - [Customize the Configuration](#customize-the-configuration)
      - [Run the Project](#run-the-project)
  - [Key Features](#key-features)
  - [License](#license)
  - [Citation](#citation)
  - [How to Contribute?](#how-to-contribute)
  - [Acknowledgments](#acknowledgments)
  - [Contact](#contact)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->


## Dataset Formats

The dataset is available in various formats to cater to different needs:

- SQLite: [Link to SQLite dump file](link/to/sqlite/dump)
- PostgreSQL: [Link to PostgreSQL dump file](link/to/psql/dump)
- CSV: [Link to CSV file](link/to/csv/file)
- TSV: [Link to TSV file](link/to/tsv/file)
- XLSX: [Link to XLSX file](link/to/xlsx/file)

Feel free to choose the format that best suits your requirements.

## NLP Model

We have developed a state-of-the-art NLP model for classifying news articles. The model can predict the type and tags of a news article, making it a valuable tool for various applications.

## <a name='Requirements'></a>Requirements
### <a name='Python-Compatibility'></a>**Python Compatibility**
This bot is written entirely in python. tested versions are `python 3.11`, `3.10`, `3.9`, `3.8`, `3.7` while older versions should not cause any problem, we recommend using the latest version of `python3`.

### <a name='Dependencies'></a>**Dependencies**
This package requires the following packages:
* [AsyncIO](https://docs.python.org/3/library/asyncio.html "AsyncIO HomePage") - asyncio is a library to write concurrent code using the async/await syntax.
* [AIOHTTP](https://docs.aiohttp.org/en/stable/ "AIOHTTP HomePage") - Asynchronous HTTP Client/Server for `asyncio` and Python.
* [SQLAlchemy](https://www.sqlalchemy.org/ "SQLAlchemy Github") - SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
* [BS4](https://www.crummy.com/software/BeautifulSoup/ "BeautifulSoup HomePage") - a Python library designed for quick turnaround projects like screen-scraping. 
* [Psycopg](https://www.psycopg.org/ "SQLAlchemy Github") - Psycopg is the most popular `PostgreSQL` adapter for the Python programming language
* [aiosqlite](https://github.com/omnilib/aiosqlite "AIOSQLite Github") - asyncio bridge to the standard `sqlite3` module
  

## <a name='Instructions'></a>Instructions

### <a name='Scrap data'></a>Scrap data
Before you begin, ensure you have the following installed:

- `Python` (version `3.11.5`)
- `Git`

#### Clone the Repository

```bash
git clone https://github.com/AbrLabs/JameJamCorpus
cd JameJamCorpus
```

#### Create and Activate Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Install Requirements

```python
pip install -r requirements.txt
```

### How to Work

### Customize the Configuration

Edit the `jamejam/config.py` file to suit your needs. This file typically contains configuration parameters for your project.

```python
"""Configurations for the package"""

# ? Base url of the website
BASE_URL = "https://jamejamonline.ir/fa/news/"

# ? Start and end of dynamic id range
START = 1
END = 1433528

# ? Set the maximum number of concurrent calls per second
MAX_CALLS_PER_SECOND = 1024

# ? Database (postgresql offers better performance)
#! postgresql
# DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/db_name"

#! sqlite
DATABASE_URL = "sqlite+aiosqlite:///data.db"

# ? Logging
DEBUG = True
DATABASE_LOGGING = False

```

#### Run the Project

Execute the following command to run the project:

```bash
python main.py
```

This will start the application, and you should see the output in the console.

## <a name='Key-Features'></a>Key Features
Some of the key feature are listed below. For more information, please refer to the Documentation.
* **Modular** - Highly modular and can be easily extended.
* **Easy to Use** - Easy to customize the interface and messages.
* **Diverse** - Can be used for a wide range of purposes.

* **Fast** - Build with the fastest performing asynchronus libraries to achieve high performance.

## <a name='License'></a>License
This project is licensed under the [GPL-3 License](link/to/license).


## Citation

```
@article{
    title={name of my article},
    author={Mohammadreza Amani, Mobina Afshari},
    journal={journal 2023},
    year={2023}
}
```
## How to Contribute?
We welcome contributions to enhance the dataset and improve the NLP model. If you have suggestions, bug reports, or want to contribute code, please follow the guidelines in [CONTRIBUTING.md](link/to/contributing/file).


## Acknowledgments

We would like to express our gratitude to the [Jam-e Jam Online](https://jamejamonline.ir) website for providing valuable news content for this dataset.


## Contact

The `Jam-e Jam` dataset is free to the academic community for research purpose usage only.

For any questions about this dataset please contact the authors by sending email to and [more.amani@yahoo.com](mailto:more.amani@yahoo.com) and [mobina.afshari@aut.ac.ir](mailto:mobina.afshari@aut.ac.ir).

