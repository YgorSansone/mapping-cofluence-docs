from invocation import Requests
from parser import Parser
from os import environ as env
from dotenv import load_dotenv
load_dotenv()


if __name__ == "__main__":
    print("running")
    request = Requests()

    parser = Parser()

    url = f"{request.url_root}rest/api/content/{env['SPACE_ID']}/child/page?type=page"

    space_content = parser.parser_requests.get_info(url)

    parser.add_first_page()
    parser.extract_list_of_page_ids(space_content)

    request.send_to_google_sheets(parser.pages, parser.skip_pages)
