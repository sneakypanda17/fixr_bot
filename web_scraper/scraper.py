import os
import requests
from bs4 import BeautifulSoup
import json


def url_scraper():
    # The URL of the website you want to scrape
    url = "https://fixr.co/organiser/timepiece"

    # Sending a GET request to the website
    response = requests.get(url)

    # Parsing the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Create a list to store the event data
    event_list = []

    # Find all elements with class "sc-6fd82db5-0 gWmhDs"
    for element in soup.find_all(class_="sc-6fd82db5-0 gWmhDs"):
        # Extract the text content of each element
        element_text = element.text.strip()

        # Split the text at "2024" and keep only the first part
        element_text = element_text.split("2024")[0].strip()

        # Extract the URL of each element and add "fixr.co" to the start
        element_url = "fixr.co" + element['href']

        # Create a dictionary for each event
        event = {
            "date": element_text,
            "url": element_url
        }

        # Add the event to the event list
        event_list.append(event)

    # Specify the file path relative to the current directory
    file_path = os.path.join(os.path.dirname(__file__), "events.json")

    # Dump the contents of event_list to a JSON file
    with open(file_path, 'w') as file:
        json.dump(event_list, file, indent=4)
