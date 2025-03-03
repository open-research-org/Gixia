from datetime import datetime
import json
import kagglehub
from tqdm import tqdm

from gixia.core.database import Database
from gixia.core.paper import Paper

# Download latest version
path = kagglehub.dataset_download("Cornell-University/arxiv")
path = f'{path}/arxiv-metadata-oai-snapshot.json'
print(f'Downloaded Arxiv dataset to {path}')

database = Database()
batch_size = 10000
with open(path, 'r') as f:
    total_lines = sum(1 for _ in f)
    f.seek(0)
    papers = []
    for line in tqdm(f, desc='Loading Arxiv dataset', total=total_lines):
        data = json.loads(line)
        paper = Paper(
            id=data['id'],
            title=data['title'],
            authors=data['authors'].split(', '),
            abstract=data['abstract'],
            updated=datetime.strptime(data['update_date'], '%Y-%m-%d'),
            arxiv_metadata=data
        )
        papers.append(paper)
        if len(papers) == batch_size:
            database.add_papers(papers)
            papers = []
    if len(papers) > 0:
        database.add_papers(papers)