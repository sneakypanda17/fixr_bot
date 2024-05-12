import pandas as pd
import random
import os
import secrets
import string

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
        number = str(random.randint(100, 999))  # Two-digit number
        symbol = random.choice(["!", "?", "$", "%"])  # One symbol
        password = f"{word}{number}{symbol}"
        return password

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
            return firstname, surname, email, password

        # Generate 10 random emails with associated names and passwords
        data = [generate_email(firstnames, surnames) for _ in range(number_of_emails)]
        data_df = pd.DataFrame(data, columns=['Firstname', 'Surname', 'Email', 'Password'])

        # Save to CSV in the same directory as the script
        output_path = os.path.join(base_dir, 'generated_credentials.csv')
        data_df.to_csv(output_path, index=False)
        print("Data has been saved to 'generated_credentials.csv'")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Direct usage
if __name__ == "__main__":
    credential_generator()
