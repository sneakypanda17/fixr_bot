import json
import os

def id_generator():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the file path for events.json
    events_file_path = os.path.join(current_dir, 'events.json')

    # Open the events.json file
    with open(events_file_path) as file:
        data = json.load(file)

    # Extract the unique event IDs from the URLs
    event_ids = []
    for event in data:
        url = event['url']
        event_id = url.rsplit('-', 1)[-1]
        if event_id not in event_ids:
            event_ids.append(event_id)
            event['ID'] = event_id  # Add the event ID as a new category

    # Save the updated data back to the events.json file
    with open(events_file_path, 'w') as file:
        json.dump(data, file, indent=4)
