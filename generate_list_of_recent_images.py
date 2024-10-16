import requests
import json

"""
To run this script you need the requests library. You can install it with pip:
in a venv as follows:

$ python3 -mvenv .venv
$ source .venv/bin/activate
$ pip install requests
$ python3 ./list_current_images.py > list_of_recent_images.txt
$ deactivate
$ rm -rf .venv

you will now have a file called list_of_recent_images.txt with the list of images
"""

def make_api_request(page, page_size):
    url = "https://registry.hub.docker.com/v2/repositories/jrottenberg/ffmpeg/tags"
    params = {"page": page, "page_size": page_size}
    response = requests.get(url, params=params)
    return response.json()

def process_data(data):
    data = json.loads(data)
    sorted_data = sorted(data, key=lambda x: x["name"], reverse=True)
    for item in sorted_data:
        if item["tag_status"].lower() == "active":
            size_mb = round(item["full_size"] / 1048576)
            name_padding = " " * (20 - len(item["name"]))
            size_padding = " " * (8 - len(str(size_mb)))
            last_updated = item["last_updated"][:10]
            # print("-" * 50)
            # print(json.dumps(item, indent=4))
            print(f"{item['name']}{name_padding}{size_mb}mb{size_padding}{last_updated}")
            # print(f'{item["last_updater_username"]}')

def main():
    page = 1
    page_size = 100
    data = []

    while True:
        response = make_api_request(page, page_size)
        data.extend(response["results"])

        if len(response["results"]) < page_size:
            break

        page += 1

    process_data(json.dumps(data))

if __name__ == "__main__":
    main()