#Import necessary libraries 
import time
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

# Configure Chrome options
driver = None
print("Configuring Chrome options...")
options = Options()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
options.add_argument(f"user-agent={user_agent}")

try:
    print("Initializing Chrome driver...")
    driver = webdriver.Chrome(service=ChromeService(), options=options)

    print("Opening beer search page...")
    driver.get("https://soysuper.com/search?q=cervezas&category=bebidas%2Fcerveza")
    time.sleep(np.random.randint(1, 5))

    print("Scrolling to load all beers...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(np.random.randint(1, 5))
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Reached end of page.")
            break
        last_height = new_height

    print("Extracting beer links...")
    beers_links = []
    product_elements = driver.find_elements(By.CSS_SELECTOR, "a.name")
    for a in product_elements:
        try:
            href = a.get_attribute("href")
            if not href:
                continue
            full_url = href if not href.startswith("/p/") else "https://soysuper.com" + href
            if full_url not in beers_links:
                beers_links.append(full_url)
        except Exception as e:
            print(f"Extracting link failed: {e}")
    print(f"Found {len(beers_links)} beer links.")

    data = []
    for idx, link in enumerate(beers_links, start=1):
        print(f"Processing {idx}/{len(beers_links)}: {link}")
        try:
            driver.get(link)
            time.sleep(np.random.randint(1, 5))

            # Name
            name = ""
            try:
                name = driver.find_element(By.CSS_SELECTOR, "h1.withpagination").text.strip()
            except Exception:
                print("Name not found.")

            # Price and lot
            price = ""
            lot = ""
            try:
                price_section = driver.find_element(By.CSS_SELECTOR, "span.price")
                if price_section.find_elements(By.TAG_NAME, "strong"):
                    price = price_section.find_element(By.TAG_NAME, "strong").text.strip()
                    lot = price_section.text.replace(price, "").strip()
            except Exception:
                print("Price section not found.")

            # Supermarket prices
            supermarkets = []
            try:
                rows = driver.find_elements(By.CSS_SELECTOR, "tr")
                for row in rows:
                    try:
                        icon = row.find_element(By.CSS_SELECTOR, "th i")
                        title = icon.get_attribute("title").strip()
                        price_cell = row.find_element(By.CSS_SELECTOR, "td.price").text.strip()
                        supermarkets.append(f"{title}: {price_cell}")
                    except Exception:
                        continue
            except Exception:
                print("Supermarket rows not found.")

            # Description
            description = ""
            try:
                description = driver.find_element(By.CSS_SELECTOR, "section.product__description").text.strip()
            except Exception:
                print("Description not found.")

            # Image URL
            image_url = ""
            try:
                image_url = driver.find_element(By.CSS_SELECTOR, "div.product__image img").get_attribute("src")
            except Exception:
                print("Image URL not found.")

            data.append({
                "Product Link": link,
                "Name": name,
                "Main Price": price,
                "Lot Size": lot,
                "Supermarkets and Prices": "; ".join(supermarkets),
                "Description": description,
                "Image": image_url
            })
        except Exception as e:
            print(f"Scraping {link} failed: {e}")

    print("Saving data to Excel...")
    df = pd.DataFrame(data)
    df.to_excel("beers_spain.xlsx", index=False)
    print("Data saved to 'beers_spain.xlsx'.")

except Exception as e:
    print(f"Script failed: {e}")
