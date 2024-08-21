"""
Load data from the ArXiv Kaggle snapshot file.
The file cut-off date is 2024-05-07.
The file contains only metadata, not full text. The metadata includes the following fields:
    id: ArXiv ID (can be used to access the paper, see below)
    submitter: Who submitted the paper
    authors: Authors of the paper
    title: Title of the paper
    comments: Additional info, such as number of pages and figures
    journal-ref: Information about the journal the paper was published in
    doi: [https://www.doi.org](Digital Object Identifier)
    abstract: The abstract of the paper
    categories: Categories / tags in the ArXiv system
    versions: A version history
File location is `D:/Data/arxiv-metadata-oai-snapshot.json`.
"""

import json
import os

# Define the file path
file_path = 'D:/Data/arxiv-metadata-oai-snapshot.json'

# Check if the file exists
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    exit()

# Load the data from the file
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Display the first record
print(data[0])

# Display the number of records
print(f"Number of records: {len(data)}")

# Find the earliest and latest dates in the dataset
dates = [record['created'] for record in data]
earliest_date = min(dates)
latest_date = max(dates)
print(f"Earliest date: {earliest_date}")
print(f"Latest date: {latest_date}")
