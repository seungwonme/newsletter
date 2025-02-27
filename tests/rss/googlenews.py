from datetime import datetime, timedelta

import requests

from src.agent.utils.file_utils import save_text_to_unique_file

# https://discordbot.tistory.com/17


def main():
    url = "https://news.google.com/rss/search?"
    # Calculate the date for yesterday
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # Construct the query with the dynamic date
    query = f"?q=economy site:cnn.com after:{yesterday}"
    response = requests.get(url + query)

    if response.status_code == 200:
        save_text_to_unique_file(str(response.content))
    else:
        print("Request failed with status code:", response.status_code)


if __name__ == "__main__":
    main()
