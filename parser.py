import json

from document import Document
from invocation import Requests
from os import environ as env
from dotenv import load_dotenv
load_dotenv()

class Parser:
    def __init__(self):
        self.pages = list()
        self.skip_pages = list()
        self.skip_labels = json.loads(env['SKIP_LABELSs'])
        self.parser_requests = Requests()

    def skip_page_by_label(self, labels):
        if labels:
            output_labels = '|'.join([d['name'] for d in labels])
            for label in labels:
                if label["name"] in self.skip_labels:
                    return {"skip": True, "list": output_labels}
            return {"skip": False, "list": output_labels}
        return {"skip": False, "list": ""}

    def add_first_page(self):
        url = f'{self.parser_requests.url_root}/rest/api/content/{env["SPACE_ID"]}'
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

                url = f'{self.parser_requests.url_root}/rest/api/content/search?cql=parent={item.get("id")}'
                self.extract_list_of_page_ids(
                    self.parser_requests.get_info(url))

        return