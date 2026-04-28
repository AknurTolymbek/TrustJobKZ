import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
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


def get_description_hh(driver, url: str) -> str:
    """Собирает описание с hh.kz"""
    try:
        driver.get(url)
        time.sleep(1.5)
        desc = driver.find_element(By.CSS_SELECTOR, "[data-qa='vacancy-description']")
        return clean_html(desc.get_attribute("innerHTML"))
    except:
        return ""


def get_description_olx(driver, url: str) -> str:
    """Собирает описание с olx.kz"""
    try:
        driver.get(url)
        time.sleep(1.5)
        desc = driver.find_element(By.CSS_SELECTOR, "[data-cy='ad_description']")
        return clean_html(desc.get_attribute("innerHTML"))
    except:
        return ""


def collect_descriptions():
    df = pd.read_csv("../data/raw/all_raw.csv")
    df["description"] = df["description"].astype(str).replace("nan", "")  # ← добавь это
    driver = create_driver()

    total = len(df)
    print(f"Total vacancies: {total}")
    print("We are starting to collect descriptions...\n")

    for i, row in df.iterrows():
        # Пропускаем если описание уже есть
        if pd.notna(row["description"]) and row["description"] != "":
            continue

        if row["source"] == "hh.kz":
            desc = get_description_hh(driver, row["url"])
        else:
            desc = get_description_olx(driver, row["url"])

        df.at[i, "description"] = desc

        # Сохраняем каждые 50 вакансий — на случай если что-то упадёт
        if (i + 1) % 50 == 0:
            df.to_csv("../data/raw/all_raw.csv", index=False)
            print(f"Progress: {i + 1}/{total} — saved")

    driver.quit()

    # Финальное сохранение
    df.to_csv("../data/raw/all_raw.csv", index=False)

    filled = df["description"].notna().sum()
    empty = df["description"].isna().sum()
    print(f"\nDone!")
    print(f"With description: {filled} из {total}")
    print(f"Without description: {empty} (links didn't open)")


if __name__ == "__main__":
    collect_descriptions()