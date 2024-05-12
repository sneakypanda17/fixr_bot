import pandas as pd
import random
def email_generator():
    
    # Load the CSV files
    firstnames_df = pd.read_csv('raw_data/firstnames.csv')  # Update the path as necessary
    surnames_df = pd.read_csv('raw_data/surnames.csv')      # Update the path as necessary

    # Extract columns as lists
    firstnames = firstnames_df['firstname'].tolist()
    surnames = surnames_df['surname'].tolist()

    def generate_email(firstnames, surnames, domain='yahoo.com'):
        """Generates an email using a random first name, surname, and a random 4-digit number."""
        firstname = random.choice(firstnames)
        surname = random.choice(surnames)
        number = random.randint(1000, 9999)  # Generates a random four digit number
        email = f"{firstname.lower()}.{surname.lower()}{number}@{domain}"
        return firstname, surname, email

    # Generate 10 random emails with associated names
    data = [generate_email(firstnames, surnames) for _ in range(100)]
    data_df = pd.DataFrame(data, columns=['Firstname', 'Surname', 'Email'])

    # Save to CSV
    data_df.to_csv('generated_emails.csv', index=False)
    print("Data has been saved to 'generated_emails.csv'")
email_generator()