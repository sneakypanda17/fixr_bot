import scraper
import id_generator
import os

file_path = os.path.join(os.path.dirname(__file__), "events.json")

    # Dump the contents of event_list to a JSON file
with open(file_path, 'w') as file:
    file.truncate

def main():
    scraper.url_scraper()
    id_generator.id_generator()

main()