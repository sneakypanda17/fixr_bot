import csv, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--ignore-certificate-errors")
    chromedriver_path = r"C:\Users\danie\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    return webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)

def register_account(driver, account, writer):
    try:
        driver.get("https://fixr.co/login")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "b[data-testid='register-button']"))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "user-profile-first-name"))).send_keys(account['Firstname'])
        driver.find_element(By.ID, "user-profile-last-name").send_keys(account['Surname'])
        driver.find_element(By.ID, "user-profile-dob").send_keys(account['Birthday'])
        driver.find_element(By.ID, "user-profile-email").send_keys(account['Email'])
        driver.find_element(By.NAME, "confirmEmail").send_keys(account['Email'])
        driver.find_element(By.ID, "user-profile-phone-number").send_keys(account['Phone Number'])
        driver.find_element(By.ID, "user-profile-password").send_keys(account['Password'])
        driver.find_element(By.NAME, "confirmPassword").send_keys(account['Password'])
        driver.find_element(By.ID, "user-profile-gender-o").click()  # Click on 'Prefer not to disclose'
        driver.find_element(By.ID, "user-profile-marketing-false").click()  # Opt out of marketing
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to bottom
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'REGISTER')]"))).click()  # Submit form
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Book tickets.')]")))  # Confirm success
        print(f"Account creation successful for {account['Email']}")
        writer.writerow(account)  # Write success to CSV
    except Exception as e:
        print(f"An error occurred for {account['Email']}: {str(e)}")
        driver.save_screenshot(f"error_{account['Email']}.png")  # Save screenshot on error

if __name__ == "__main__":
    driver = setup_driver()
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        credentials_csv_path = os.path.join(current_dir, '../credential_generator/credentials.csv')
        with open(credentials_csv_path, newline='', encoding='utf-8') as infile, open(os.path.join(current_dir,'unused_accounts.csv'), 'a', newline='', encoding='utf-8') as outfile:
            reader = csv.DictReader(infile)
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            if outfile.tell() == 0: writer.writeheader()  # Write header if file is empty
            for account in reader: register_account(driver, account, writer)
    finally:
        driver.quit()
