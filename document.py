from datetime import datetime
from os import environ as env

from dotenv import load_dotenv
load_dotenv()

class Document:
    def __init__(self, page_title, page_id, last_updated_user, last_updated_data, create_data, create_user, labels):
        self.page_title = page_title
        self.page_id = page_id
        self.last_updated_user = last_updated_user
        self.last_updated_data = last_updated_data
        self.create_data = create_data
        self.create_user = create_user
        self.labels = labels

    def compare_dates(self, date):
        start_date = datetime.strptime(date.split("T")[0], "%Y-%m-%d")
        end_date = datetime.strptime(str(datetime.now().date()), "%Y-%m-%d")
        return end_date - start_date

    def create_dict(self):
        return {"id": self.page_id,
                "page_title": self.page_title,
                "last_updated_user": self.last_updated_user,
                "last_updated_date": self.last_updated_data,
                "days_from_last_update": self.compare_dates(self.last_updated_data),
                "days_from_creation": self.compare_dates(self.last_updated_data),
                "create_date": self.create_data,
                "create_user": self.create_user,
                "labels": self.labels,
                "page_link": f"{env['URL_ROOT']}/engineering/pages/{self.page_id}",
                }
