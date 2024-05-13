import os
import requests
from bs4 import BeautifulSoup
import json

def url_scraper():
    # The URL of the website you want to scrape
    url = "https://fixr.co/organiser/timepiece"

    # Add headers to mimic a browser visit
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

    # Sending a GET request to the website with headers
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parsing the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Create a list to store the event data
        event_list = []

        # Find all <a> tags that contain '/event/' in their 'href' attribute
        for element in soup.find_all('a', href=True):
            href = element['href']
            if '/event/' in href:
                # Extract the text content of each element
                element_text = element.text.strip()

                # Correctly form the URL
                element_url = "https://fixr.co" + href if href.startswith('/') else href

                # Assuming the event date might be in the text and trimming extraneous text
                element_text = element_text.split("2024")[0].strip()

                # Create a dictionary for each event
                event = {
                    "date": element_text,
                    "url": element_url
                }

                # Add the event to the event list
                event_list.append(event)

        # Extract and add event IDs
        event_ids = []
        for event in event_list:
            url = event['url']
            event_id = url.rsplit('-', 1)[-1]
            if event_id not in event_ids:
                event_ids.append(event_id)
                event['ID'] = int(event_id)  # Add the event ID as a new key in the dictionary


        # Specify the file path to save it in the same directory as the script
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'events.json')

        # Dump the contents of event_list to a JSON file
        with open(file_path, 'w') as file:
            json.dump(event_list, file, indent=4)
    else:
        print("Failed to retrieve data, HTTP Status:", response.status_code)

url_scraper()
