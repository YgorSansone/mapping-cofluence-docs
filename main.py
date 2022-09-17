import json
import requests
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
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


class Parser:
    def __init__(self, parser_requests):
        self.pages = list()
        self.skip_pages = list()
        self.skip_labels = json.loads(env['SKIP_LABELSs'])
        self.parser_requests = parser_requests

    def skip_page_by_label(self, labels):
        if labels:
            output_labels = '|'.join([d['name'] for d in labels])
            for label in labels:
                if label["name"] in self.skip_labels:
                    return {"skip": True, "list": output_labels}
            return {"skip": False, "list": output_labels}
        return {"skip": False, "list": ""}

    def add_first_page(self):
        url = f'{requests.url_root}/rest/api/content/{env["SPACE_ID"]}'
        content = dict(json.loads(self.parser_requests.get_info(url)))
        if content is None:
            return
        elif content.get('type') == 'page':
            return self.extract_itens(content)
        return

    def extract_itens(self, item):
        labels = item["metadata"]["labels"]["results"]
        check_label = self.skip_page_by_label(labels)
        docs = Document(page_title=item["title"],
                        create_data=item["history"]["createdDate"],
                        last_updated_data=item["history"]["lastUpdated"]["when"],
                        last_updated_user=item["history"]["createdBy"]["publicName"],
                        page_id=item.get("id"),
                        create_user=item["history"]["createdBy"]["publicName"],
                        labels=check_label["list"]
                        )
        if check_label["skip"] == False:
            return self.pages.append(docs.create_dict())

        return self.skip_pages.append(docs.create_dict())

    def extract_list_of_page_ids(self, content):
        as_json = json.loads(content)
        content_list = dict(as_json).get('results')
        if content_list is None:
            return
        for item in content_list:
            if item.get('type') == 'page':
                self.extract_itens(item)

                url = f'{requests.url_root}/rest/api/content/search?cql=parent={item.get("id")}'
                self.extract_list_of_page_ids(
                    self.parser_requests.get_info(url))
                return

        return


class Requests:
    def __init__(self):
        self.session = requests
        self.url_root = env['URL_ROOT']

    def get_info(self, url):
        querystring = {
            "expand": "metadata.labels,childTypes.page,history.lastUpdated"}
        headers = {
            "Authorization": "Basic " + env['AUTHORIZATION']}
        response = self.session.get(url, headers=headers, params=querystring)
        return str(response.text)

    def send_to_google_sheets(self, parser):
        csv_file_name = "output.csv"
        output_df = pd.DataFrame(parser.pages)
        output_df.to_csv(csv_file_name, sep=',', encoding='utf-8')

        output_skip_pages_df = pd.DataFrame(parser.skip_pages)
        output_skip_pages_df.to_csv(
            "output_skip_pages.csv", sep=',', encoding='utf-8')

        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'client_secret.json', scope)
        client = gspread.authorize(credentials)

        spreadsheet = client.open('CSV-to-Google-Sheet')
        with open(csv_file_name, 'r') as file_obj:
            content = file_obj.read()
            client.import_csv(spreadsheet.id, data=content)


if __name__ == "__main__":
    print("running")
    requests = Requests()

    parser = Parser(requests)

    url = f"{requests.url_root}rest/api/content/{env['SPACE_ID']}/child/page?type=page"

    space_content = parser.parser_requests.get_info(url)

    parser.add_first_page()
    parser.extract_list_of_page_ids(space_content)

    requests.send_to_google_sheets(parser)
