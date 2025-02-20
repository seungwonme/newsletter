# https://gomgomi.github.io/web/scrap-using-google-google-cse/
# https://developers.google.com/custom-search/v1/overview?hl=ko

import os

import requests
from dotenv import load_dotenv

from tests.utils import save_text_to_unique_file

load_dotenv()


def main():
    api_key = os.getenv("GOOGLE_CSE_API_KEY")
    cx = os.getenv("GOOGLE_CSE_ID")
    url = "https://customsearch.googleapis.com/customsearch/v1"
    query = "economy site:cnn.com after:2025-02-17"
    params = {
        "key": api_key,
        "cx": cx,
        "q": query,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        print("Request was successful")
        save_text_to_unique_file(response.content.decode("utf-8"))
    else:
        print("Request failed with status code:", response.status_code)


if __name__ == "__main__":
    main()
