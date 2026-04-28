import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from utils import clean_html


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver


def parse_hh(pages: int = 10) -> pd.DataFrame:
    driver = create_driver()
    vacancies = []

    for page in range(pages):
        url = f"https://hh.kz/search/vacancy?area=40&per_page=50&page={page}"
        print(f"Page {page + 1}/{pages}: {url}")

        driver.get(url)
        time.sleep(2)

        cards = driver.find_elements(By.CSS_SELECTOR, "[data-qa='vacancy-serp__vacancy']")

        if not cards:
            print("No vacancies found, stopping")
            break

        for card in cards:
            try:
                title = card.find_element(By.CSS_SELECTOR, "[data-qa='serp-item__title']").text
            except:
                title = ""

            try:
                company = card.find_element(By.CSS_SELECTOR, "[data-qa='vacancy-serp__vacancy-employer']").text
                has_company = 1
            except:
                company = None
                has_company = 0

            try:
                salary = card.find_element(By.CSS_SELECTOR, "[data-qa='vacancy-serp__vacancy-compensation']").text
                has_salary = 1
            except:
                salary = None
                has_salary = 0

            try:
                link = card.find_element(By.CSS_SELECTOR, "[data-qa='serp-item__title']").get_attribute("href")
            except:
                link = ""

            vacancies.append({
                "title":            title,
                "company_name":     company,
                "has_company_name": has_company,
                "salary":           salary,
                "has_salary":       has_salary,
                "url":              link,
                "source":           "hh.kz",
                "description":      "",
                "label":            None
            })

        print(f"Collected on page: {len(cards)}vacancies")

    driver.quit()

    if not vacancies:
        print("Data not collected.")
        return pd.DataFrame()

    df = pd.DataFrame(vacancies)
    print(f"\nTotal collected: {len(df)} vacancies")
    print("Saving..")

    df.to_csv("../data/raw/hh_raw.csv", index=False)
    print("Done → data/raw/hh_raw.csv")
    return df


if __name__ == "__main__":
    parse_hh(pages=10)