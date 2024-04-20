import pandas as pd
import random

# Load the CSV files
firstnames_df = pd.read_csv('raw_data/firstnames.csv')  # Update the path as necessary
surnames_df = pd.read_csv('raw_data/surnames.csv')      # Update the path as necessary
print(firstnames_df.head)

'''
# Extract columns as lists
firstnames = firstnames_df['firstname'].tolist()
surnames = surnames_df['surname'].tolist()

def generate_email(firstnames, surnames, domain='yahoo.com'):
    """Generates an email using a random first name, surname, and a random 4-digit number."""
    firstname = random.choice(firstnames)
    surname = random.choice(surnames)
    number = random.randint(1000, 9999)  # Generates a random four digit number
    email = f"{firstname.lower()}.{surname.lower()}{number}@{domain}"
    return email

# Generate 10 random emails
emails = [generate_email(firstnames, surnames) for _ in range(10)]

# Save to CSV
emails_df = pd.DataFrame(emails, columns=['Email'])
emails_df.to_csv('generated_emails.csv', index=False)
print("Emails have been saved to 'generated_emails.csv'")

'''