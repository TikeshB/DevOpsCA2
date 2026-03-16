import time

import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1200,900")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def base_url():
    # Target the local file path. Adjust if running via a local server.
    return "file://" + __import__("os").path.abspath("index.html")


def test_form_page_loads(driver, base_url):
    driver.get(base_url)
    assert "Student Feedback Registration" in driver.title


def test_successful_submission_shows_toast(driver, base_url):
    driver.get(base_url)

    driver.find_element(By.ID, "name").send_keys("Aisha Khan")
    driver.find_element(By.ID, "email").send_keys("aisha.khan@example.com")
    driver.find_element(By.ID, "phone").send_keys("9876543210")
    driver.find_element(By.ID, "department").click()
    driver.find_element(By.CSS_SELECTOR, "#department option[value='Computer Science']").click()
    driver.find_element(By.CSS_SELECTOR, "input[name='gender'][value='Female']").click()
    driver.find_element(By.ID, "comments").send_keys(
        "The course structure was great and the instructor explained all concepts clearly."
    )

    driver.find_element(By.ID, "submitBtn").click()

    toast = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "toast"))
    )
    assert "Feedback submitted successfully" in toast.text


def test_validation_errors_for_blank_required_fields(driver, base_url):
    driver.get(base_url)

    driver.find_element(By.ID, "submitBtn").click()

    # Expect error messages to show
    for field in ["name", "email", "phone", "department", "gender", "comments"]:
        error = driver.find_element(By.CSS_SELECTOR, f".field__error[data-for='{field}']")
        assert error.text.strip() != ""


def test_invalid_email_and_phone_validation(driver, base_url):
    driver.get(base_url)

    driver.find_element(By.ID, "name").send_keys("Test User")
    driver.find_element(By.ID, "email").send_keys("not-an-email")
    driver.find_element(By.ID, "phone").send_keys("12345")
    driver.find_element(By.ID, "department").click()
    driver.find_element(By.CSS_SELECTOR, "#department option[value='Information Technology']").click()
    driver.find_element(By.CSS_SELECTOR, "input[name='gender'][value='Male']").click()
    driver.find_element(By.ID, "comments").send_keys("This feedback is testing email and phone validation.")

    driver.find_element(By.ID, "submitBtn").click()

    email_error = driver.find_element(By.CSS_SELECTOR, ".field__error[data-for='email']").text
    phone_error = driver.find_element(By.CSS_SELECTOR, ".field__error[data-for='phone']").text

    assert "valid email" in email_error.lower()
    assert "10 digits" in phone_error.lower()


def test_reset_button_clears_fields(driver, base_url):
    driver.get(base_url)

    driver.find_element(By.ID, "name").send_keys("Reset Test")
    driver.find_element(By.ID, "email").send_keys("reset@test.com")
    driver.find_element(By.ID, "phone").send_keys("9876543210")

    driver.find_element(By.ID, "resetBtn").click()

    time.sleep(0.5)

    assert driver.find_element(By.ID, "name").get_attribute("value") == ""
    assert driver.find_element(By.ID, "email").get_attribute("value") == ""
    assert driver.find_element(By.ID, "phone").get_attribute("value") == ""
