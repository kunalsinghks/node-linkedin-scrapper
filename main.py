#add image uri

import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep

def extract_key_value_pair(driver, xpath):
    try:
        element = driver.find_element(By.XPATH, xpath)
        category = element.find_element(By.TAG_NAME, 'dt').text.strip()
        value = element.find_element(By.TAG_NAME, 'dd').text.strip()
        return category, value
    except Exception as e:
        print(f"Error extracting key-value pair: {e}")
        return None, None

def scrape_company_data(url):
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Initialize Chrome WebDriver
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

        driver.get(url)

        # Wait for the page to load
        sleep(5)  

        try:
            # Find the pop-up window element
            popup_element = driver.find_element(By.XPATH, '//*[@id="organization_guest_contextual-sign-in"]/div/section/button').click()
            print("Pop-up window closed successfully.")
        except Exception as e:
            print(f"No pop-up window found or an error occurred: {e}")

        # Extract company data
        company_data = {}

        # Include URL
        company_data['url'] = url

        company_name = driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/section/div/div[2]/div[1]/h1').text.strip()
        about_us = driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/section[1]/div/p').text.strip()
        company_data['about'] = about_us
        company_data['companyName'] = company_name

        xpaths = [
            '//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[1]',  # Website
            '//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[2]',  # Industry
            '//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[3]',  # Company Size
            '//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[4]',  # Headquarters
            '//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[5]',  # Founded
            '//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[6]',  # Type
            '//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[7]'   # Specialties
        ]

        # Populate available values
        for xpath in xpaths:
            category, value = extract_key_value_pair(driver, xpath)
            if category:
                camel_case_key = category.replace(" ", "").lower()
                if camel_case_key == 'companysize':
                    camel_case_key = 'companySize'  # Convert 'companysize' to 'companySize'
                company_data[camel_case_key] = value

        # Scrape profile image URI
        try:
            profile_image_element = driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/section/div/div[1]/img')
            image_uri = profile_image_element.get_attribute("src")
            company_data['avatarUrl'] = image_uri
        except Exception as e:
            print(f"Error scraping profile image URI: {e}")

        # Close the WebDriver
        driver.quit()

        # Reorder the dictionary keys
        reordered_keys = [
            "url", "website", "companyName", "about","companySize", "headquarters", "industry","type", "specialties", "avatarUrl"
        ]
        reordered_data = {key: company_data[key] for key in reordered_keys if key in company_data}

        return reordered_data

    except Exception as ex:
        print(f"An error occurred: {ex}")
        return None

# Example usage:
company_url = 'https://www.linkedin.com/company/openai'
company_data = scrape_company_data(company_url)
if company_data:
    print(json.dumps(company_data, indent=4))
    json_file_path = 'company_data.json'  
    with open(json_file_path, 'w') as jsonfile:
        json.dump(company_data, jsonfile, indent=4)
    print('Scraping completed. Data saved to:', json_file_path)
else:
    print("Scraping failed.")
