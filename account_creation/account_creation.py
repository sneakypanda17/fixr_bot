from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Replace the fields with the information to create a new account
first_name = "John"
last_name = "Doe"
email = "john.doe@example.com"
phone_number = "7400123456"
password = "secure_password123"
date_of_birth = "01/01/1990"  # Format: dd/mm/yyyy

# Initialize the Chrome WebDriver
driver = webdriver.Chrome("C:/Users/danie/Downloads/chromedriver_win32/chromedriver.exe")

try:
    # Open the registration page
    driver.get("https://fixr.co/login")
    # Wait for the 'Sign Up' link and click it
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Sign up"))
    ).click()

    # Wait and fill out the registration form
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "first_name"))
    ).send_keys(first_name)
    driver.find_element(By.NAME, "last_name").send_keys(last_name)
    driver.find_element(By.NAME, "dob").send_keys(date_of_birth)
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "email_confirmation").send_keys(email)
    driver.find_element(By.NAME, "phone_number").send_keys(phone_number)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password_confirmation").send_keys(password)

    # Select gender, preferred language, and opt-out of communications
    driver.find_element(By.XPATH, "//label[text()='Prefer not to disclose']").click()
    driver.find_element(By.XPATH, "//option[text()='English']").click()
    driver.find_element(By.XPATH, "//label[contains(text(),'opt out')]").click()

    # Submit the form
    driver.find_element(By.XPATH, "//button[contains(text(),'Register')]").click()

    # Optionally, handle post-registration tasks or checks here
    print("Registration attempted with email:", email)

finally:
    # Close the driver after a delay or based on a specific condition
    driver.quit()
