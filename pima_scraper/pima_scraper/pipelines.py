# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv


class CasePipeline:
    def open_spider(self, spider):
        self.file = open('cases.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.file, fieldnames=[
            "party_name", "case_number", "case_caption", "filing_date",
            "case_type", "status", "judge"
        ])
        self.writer.writeheader()

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if item.get("_type") == "case":
            del item["_type"]
            self.writer.writerow(item)
        return item


class DocketPipeline:
    def open_spider(self, spider):
        self.file = open('dockets.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.file, fieldnames=[
            "case_number", "event_date", "event_description", "event_result", "event_notes"
        ])
        self.writer.writeheader()

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if item.get("_type") == "docket":
            del item["_type"]
            self.writer.writerow(item)
        return item