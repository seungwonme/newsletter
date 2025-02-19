# https://gomgomi.github.io/web/scrap-using-google-google-cse/
# https://developers.google.com/custom-search/v1/overview?hl=ko

import requests

from tests.api.utils import save_text_to_unique_file


def main():
    url = "https://www.google.com/search"
    query = "?q=economy site:cnn.com after:2025-02-17"
    response = requests.get(url + query)

    if response.status_code == 200:
        print("Request was successful")
        save_text_to_unique_file(response.content.decode("utf-8"))
    else:
        print("Request failed with status code:", response.status_code)


if __name__ == "__main__":
    main()

# https://developers.google.com/custom-search/v1/overview?hl=ko
