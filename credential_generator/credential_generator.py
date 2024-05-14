import pandas as pd
import random
import os
import secrets
import string
from datetime import datetime, timedelta

def credential_generator(number_of_emails=10):
    # Define the base directory relative to the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to the words CSV
    words_path = os.path.join(base_dir, 'raw_data', 'words.csv')

    # Load words from the CSV file
    words_df = pd.read_csv(words_path)
    words_list = words_df['Word'].tolist()

    def generate_password():
        """Generates a secure, memorable password using a combination of words, numbers, and a symbol."""
        word = random.choice(words_list)
        number = str(random.randint(100, 999))  # Three-digit number
        symbol = random.choice(["!", "?", "$", "%"])  # One symbol
        password = f"{word}{number}{symbol}"
        return password

    def generate_birthday(start_year=2000, end_year=2004):
        """Generates a random birthday between start_year and end_year in the format ddmmyyyy."""
        start_date = datetime(start_year, 1, 1)
        end_date = datetime(end_year + 1, 1, 1) - timedelta(days=1)
        random_date = start_date + (end_date - start_date) * random.random()
        return random_date.strftime("%d%m%Y")

    def generate_phone_number():
        """Generates a random phone number in the format 7XX-XXX-XXXX."""
        return f"7{random.randint(10, 99)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

    try:
        # Load the CSV files
        firstnames_df = pd.read_csv(os.path.join(base_dir, 'raw_data', 'firstnames.csv'))
        surnames_df = pd.read_csv(os.path.join(base_dir, 'raw_data', 'surnames.csv'))

        # Extract columns as lists
        firstnames = firstnames_df['firstname'].tolist()
        surnames = surnames_df['surname'].tolist()

        def generate_email(firstnames, surnames, domain='yahoo.com'):
            """Generates an email using a random first name, surname, and a random 4-digit number."""
            firstname = random.choice(firstnames)
            surname = random.choice(surnames)
            number = random.randint(1000, 9999)  # Generates a random four digit number
            email = f"{firstname.lower()}.{surname.lower()}{number}@{domain}"
            password = generate_password()
            birthday = generate_birthday()
            phone_number = generate_phone_number()
            return firstname, surname, email, password, birthday, phone_number

        # Generate random emails with associated names, passwords, birthdays, and phone numbers
        data = [generate_email(firstnames, surnames) for _ in range(number_of_emails)]
        data_df = pd.DataFrame(data, columns=['Firstname', 'Surname', 'Email', 'Password', 'Birthday', 'Phone Number'])

        # Save to credentials.csv in the same directory as the script
        credentials_path = os.path.join(base_dir, 'credentials.csv')
        data_df.to_csv(credentials_path, index=False)
        print("Data has been saved to 'credentials.csv'")

        # Append new data to credentials_record.csv
        record_path = os.path.join(base_dir, 'credentials_record.csv')
        if os.path.exists(record_path):
            record_df = pd.read_csv(record_path)
            updated_record_df = pd.concat([record_df, data_df], ignore_index=True)
        else:
            updated_record_df = data_df

        updated_record_df.to_csv(record_path, index=False)
        print("Data has been appended to 'credentials_record.csv'")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Direct usage
if __name__ == "__main__":
    credential_generator(3)
