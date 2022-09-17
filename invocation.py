import requests
import pandas as pd
import gspread
from document import Document
from oauth2client.service_account import ServiceAccountCredentials
from os import environ as env

from dotenv import load_dotenv
load_dotenv()
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

    def send_to_google_sheets(self, parser_pages, parser_skip_pages):
        csv_file_name = "output.csv"
        output_df = pd.DataFrame(parser_pages)
        output_df.to_csv(csv_file_name, sep=',', encoding='utf-8')

        output_skip_pages_df = pd.DataFrame(parser_skip_pages)
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