import csv
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
    service = Service(chromedriver_path)
    return webdriver.Chrome(service=service, options=chrome_options)

def register_account(driver, account):
    try:
        driver.get("https://fixr.co/login")

        # Click on 'Create an account'
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "b[data-testid='register-button']"))
        ).click()

        # Fill out the registration form
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "user-profile-first-name"))
        ).send_keys(account['Firstname'])

        driver.find_element(By.ID, "user-profile-last-name").send_keys(account['Surname'])
        driver.find_element(By.ID, "user-profile-dob").send_keys(account['Birthday'])
        driver.find_element(By.ID, "user-profile-email").send_keys(account['Email'])
        driver.find_element(By.NAME, "confirmEmail").send_keys(account['Email'])
        driver.find_element(By.ID, "user-profile-phone-number").send_keys(account['Phone Number'])
        driver.find_element(By.ID, "user-profile-password").send_keys(account['Password'])
        driver.find_element(By.NAME, "confirmPassword").send_keys(account['Password'])

        # Click on 'Prefer not to disclose' for gender
        driver.find_element(By.ID, "user-profile-gender-o").click()

        # Opt out of marketing
        driver.find_element(By.ID, "user-profile-marketing-false").click()

        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Submit the form by clicking the REGISTER button
        register_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'REGISTER')]"))
        )
        register_button.click()

        # Wait for the confirmation element that shows booking was successful
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Book tickets.')]"))
        )

        print(f"Account creation successful for {account['Email']}")

    except Exception as e:
        print(f"An error occurred for {account['Email']}: {str(e)}")
        driver.save_screenshot(f"error_{account['Email']}.png")  # Saves a screenshot for debugging

if __name__ == "__main__":
    driver = setup_driver()
    try:
        with open('../credential_generator/credentials.csv', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for account in reader:
                register_account(driver, account)
    finally:
        driver.quit()
