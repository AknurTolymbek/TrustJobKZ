import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


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


def parse_olx(pages: int = 10) -> pd.DataFrame:
    driver = create_driver()
    vacancies = []

    for page in range(1, pages + 1):
        url = f"https://www.olx.kz/rabota/?page={page}"
        print(f"Страница {page}/{pages}: {url}")

        driver.get(url)
        time.sleep(2)

        cards = driver.find_elements(By.CSS_SELECTOR, "[data-cy='l-card']")

        if not cards:
            print("Карточки не найдены, останавливаемся")
            break

        for card in cards:
            try:
                title = card.find_element(By.CSS_SELECTOR, "h4").text
            except:
                title = ""

            try:
                salary = card.find_element(By.CSS_SELECTOR, "[data-testid='ad-price']").text
                has_salary = 1
            except:
                salary = None
                has_salary = 0

            try:
                location = card.find_element(By.CSS_SELECTOR, "[class*='css-jw5wnz']").text
            except:
                location = ""

            try:
                link = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            except:
                link = ""

            if not title:
                continue

            vacancies.append({
                "title":            title,
                "company_name":     None,
                "has_company_name": 0,
                "salary":           salary,
                "has_salary":       has_salary,
                "location":         location,
                "url":              link,
                "source":           "olx.kz",
                "description":      "",
                "label":            None
            })

        print(f" Collected: {len(cards)} vacancies")

    driver.quit()

    if not vacancies:
        print("Data not collected.")
        return pd.DataFrame()

    df = pd.DataFrame(vacancies)
    print(f"\nTotal collected: {len(df)} vacancies")
    df.to_csv("../data/raw/olx_raw.csv", index=False)
    print("Done → data/raw/olx_raw.csv")
    return df


if __name__ == "__main__":
    parse_olx(pages=10)