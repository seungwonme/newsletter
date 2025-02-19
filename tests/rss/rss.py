import requests

# https://discordbot.tistory.com/17


def main():
    url = "https://www.google.com/search"
    query = "?q=economy site:cnn.com after:2025-02-17"
    response = requests.get(url + query)

    if response.status_code == 200:
        print("Request was successful")
        print("Response content:", response.content)
    else:
        print("Request failed with status code:", response.status_code)


if __name__ == "__main__":
    main()
    main()
