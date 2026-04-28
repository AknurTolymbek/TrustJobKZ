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
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver


def get_salary(driver, url):
    try:
        driver.get(url)
        time.sleep(2)
        for selector in [
            "[data-qa='vacancy-salary-compensation-type-net']",
            "[data-qa='vacancy-salary']",
            "[data-qa='vacancy-salary-compensation-type-gross']",
        ]:
            try:
                el = driver.find_element(By.CSS_SELECTOR, selector)
                text = el.text.strip()
                if text:
                    return text, 1
            except:
                continue
        return "", 0
    except:
        return "", 0


def collect_salary():
    df = pd.read_csv("../data/raw/all_raw.csv")
    df["salary"] = df["salary"].astype(str).replace("nan", "")
    df["has_salary"] = df["has_salary"].fillna(0).astype(int)

    hh_indices = df[df["source"] == "hh.kz"].index.tolist()

    # Считаем сколько уже собрано
    already_done = df.loc[hh_indices, "has_salary"].sum()
    todo = [i for i in hh_indices if df.at[i, "has_salary"] != 1]

    print(f"hh.kz vacancies: {len(hh_indices)}")
    print(f"Already collected: {already_done}")
    print(f"Left: {len(todo)}\n")

    driver = create_driver()
    count = 0

    for i in todo:
        row = df.loc[i]

        # Перезапускаем браузер каждые 50 вакансий
        if count > 0 and count % 50 == 0:
            print(f"\nRestarting the browser on{count}th vacancy")
            try:
                driver.quit()
            except:
                pass
            time.sleep(2)
            driver = create_driver()

        salary, has_salary = get_salary(driver, row["url"])
        df.at[i, "salary"] = salary
        df.at[i, "has_salary"] = has_salary

        count += 1
        print(f"{count}/{len(todo)} | {row['title'][:35]:35} | {salary or 'нет зарплаты'}")

        # Сохраняем каждые 20
        if count % 20 == 0:
            df.to_csv("../data/raw/all_raw.csv", index=False)
            print(f"  → Saved")

    try:
        driver.quit()
    except:
        pass

    df.to_csv("../data/raw/all_raw.csv", index=False)
    filled = (df.loc[hh_indices, "has_salary"] == 1).sum()
    print(f"\nDone! With salary: {filled} из {len(hh_indices)}")


if __name__ == "__main__":
    collect_salary()