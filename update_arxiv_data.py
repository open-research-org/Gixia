import argparse
import pymongo
import re
from sickle import Sickle
import time
import tqdm

# Parse from_date and until_date from command line arguments
parser = argparse.ArgumentParser(description='Update arXiv metadata.')
parser.add_argument('--from_date', type=str, required=True, help='The date to start harvesting metadata (YYYY-MM-DD).')
parser.add_argument('--until_date', type=str, default=None, help='The date to stop harvesting metadata (YYYY-MM-DD).')
args = parser.parse_args()
from_date = args.from_date
until_date = args.until_date

# Initialize the Sickle client for the arXiv OAI-PMH interface
sickle = Sickle('http://export.arxiv.org/oai2')

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

# Connect to a MongoDB database
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['gixia']
collection = db['papers']

updated_count = 0
inserted_count = 0

for record in tqdm.tqdm(records, desc='Processing records'):
    # Extract metadata from the record and construct a new document
    id = record.metadata['id'][0]
    new_date_list = record.metadata['date']
    new_versions = [{'version': f'v{index + 1}', 'created': date} for index, date in enumerate(new_date_list)]
    new_update_date = re.search(r'<datestamp>(.*?)</datestamp>', record.header.raw).group(1)
    new_document = {
        'id': id,
        'submitter': record.metadata['submitter'][0],
        'authors': record.metadata['authors'][0],
        'title': record.metadata['title'][0],
        'categories': record.metadata['categories'][0],
        'journal-ref': record.metadata['journal-ref'][0] if 'journal-ref' in record.metadata else None,
        'doi': record.metadata['doi'][0] if 'doi' in record.metadata else None,
        'license': record.metadata['license'][0],
        'abstract': record.metadata['abstract'][0],
        'versions': new_versions,
        'update_date': new_update_date,
    }

    # Try to find an existing document with the same id
    existing_document = collection.find_one({'id': id})
    if existing_document:
        existing_update_date = existing_document['update_date']
        if new_update_date > existing_update_date:
            # Update the document with the new data
            collection.update_one({'id': id}, {'$set': new_document})
            updated_count += 1
    else:
        # Insert new data if no document with the same id exists
        collection.insert_one(new_document)
        inserted_count += 1

print(f'Updated {updated_count} documents.')
print(f'Inserted {inserted_count} documents.')

client.close()