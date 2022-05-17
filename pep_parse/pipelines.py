import csv
import datetime as dt
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'


class PepParsePipeline:
    def __init__(self):
        self.results = defaultdict(int)

    def open_spider(self, spider):
        results_dir = BASE_DIR / 'results'
        results_dir.mkdir(exist_ok=True)
        now = dt.datetime.now()
        now_format = now.strftime(DATETIME_FORMAT)
        filename = f'status_summary_{now_format}.csv'
        self.file_path = results_dir / filename

    def process_item(self, item, spider):
        status = item['status']
        self.results[status] += 1
        return item

    def close_spider(self, spider):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerows(
                [
                    ('Статус', 'Количество'),
                    *self.results.items(),
                    ('Total', sum(self.results.values()))
                ]
            )
