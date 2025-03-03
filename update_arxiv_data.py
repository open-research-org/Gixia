import argparse
from datetime import datetime
import pymongo
import re
from sickle import Sickle
import time
import tqdm

from gixia.core.database import Database
from gixia.core.paper import Paper


# Parse from_date and until_date from command line arguments
parser = argparse.ArgumentParser(description='Update arXiv metadata.')
parser.add_argument('--from-date', type=str, required=True, help='The date to start harvesting metadata (YYYY-MM-DD).')
parser.add_argument('--until-date', type=str, default=None, help='The date to stop harvesting metadata (YYYY-MM-DD).')
args = parser.parse_args()
from_date = args.from_date
until_date = args.until_date

# Initialize the Sickle client for the arXiv OAI-PMH interface
sickle = Sickle('http://export.arxiv.org/oai2')

# Collect all papers in the specified date range
records = []
batch_index = 0
resumption_token = None
metadata_format = 'arXivRaw'
while True:
    # Request records from the OAI-PMH service
    print(f'Retrieving records batch {batch_index}...')
    batch_index += 1
    records_iter = sickle.ListRecords(**{
        'metadataPrefix': metadata_format,
        'from': from_date,
        'until': until_date,
        'resumptionToken': resumption_token})
    metadata_format = None
    from_date = None
    until_date = None
    resumption_token = records_iter.resumption_token.token
    try:
        # Iterate through the records and store them
        for record in tqdm.tqdm(records_iter):
            records.append(record)
        print(f"Retrieved {len(records)} records.")
        break
    except Exception as e:
        print(f"Continue to the next batch of records after 5 seconds...")
        time.sleep(5)

# Update and insert papers to the database
database = Database()
skiped_count = 0
updated_count = 0
inserted_count = 0
papers_to_be_updated = []
papers_to_be_inserted = []

# Collect paper IDs and update dates
paper_updates = {}
for record in tqdm.tqdm(records, desc='Collecting paper IDs', total=len(records)):
    id = record.metadata['id'][0]
    update_date_str = re.search(r'<datestamp>(.*?)</datestamp>', record.header.raw).group(1)
    update_date = datetime.strptime(update_date_str, '%Y-%m-%d')
    if id in paper_updates and update_date <= paper_updates[id]['update_date']:
        continue
    paper_updates[id] = {
        'update_date': update_date,
        'record': record
    }

print(f'Getting existing papers...')
existing_papers = {paper.id: paper for paper in database.get_papers(list(paper_updates.keys()))}

# Construct papers to be updated and inserted
for paper_id, update_info in tqdm.tqdm(paper_updates.items(), desc='Processing records'):
    update_date = update_info['update_date']
    record = update_info['record']

    if paper_id in existing_papers:
        paper = existing_papers[paper_id]
        if update_date <= paper.updated:
            skiped_count += 1
            continue
        paper.title = record.metadata['title'][0]
        paper.authors = record.metadata['authors'][0].split(', ')
        paper.abstract = record.metadata['abstract'][0]
        paper.updated = update_date
        paper.arxiv_raw_metadata = record.metadata
        papers_to_be_updated.append(paper)
        updated_count += 1
    else:
        paper = Paper(
            id=paper_id,
            title=record.metadata['title'][0],
            authors=record.metadata['authors'][0].split(', '),
            abstract=record.metadata['abstract'][0],
            updated=update_date,
            arxiv_raw_metadata=record.metadata
        )
        papers_to_be_inserted.append(paper)
        inserted_count += 1

print(f'Skip {skiped_count} papers.')
print(f'Updating {len(papers_to_be_updated)} papers...')
database.update_papers(papers_to_be_updated)
print(f'Inserting {len(papers_to_be_inserted)} papers...')
database.add_papers(papers_to_be_inserted)