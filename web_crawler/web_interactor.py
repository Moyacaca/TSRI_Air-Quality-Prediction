from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

download_dir = "/Users/moya/Documents/TSRI_Air_Quality_Estimation/code/system_submit/web_crawler/"
# Path to your chromedriver
driver_path = '/Users/moya/local/bin/chromedriver-mac-x64/chromedriver' # Update this path

def delete_existing_csv_files(directory):
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            os.remove(os.path.join(directory, file))
            print(f"Deleted old file: {file}")

def crawl_website(download_dir, driver_path):
    # Set up Chrome options
    chrome_options = Options()
    # download_dir = "/Users/moya/Downloads/"
    
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "profile.default_content_settings.popups": 0
    }
    chrome_options.add_experimental_option("prefs", prefs)

    
    # Initialize the driver
    driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)

    try:
        # Navigate to the website
        driver.get("http://125.227.15.167/download")

        delete_existing_csv_files(download_dir)

        # Get the list of files before downloading
        existing_files = set(os.listdir(download_dir))
        print("Existing files:", existing_files)

        # Click the "手動指定日期" button
        css_selector = "body > div:nth-child(2) > div.d-block.px-1.mx-1.my-1 > div > div > div > div:nth-child(1) > div > button:nth-child(2)"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))).click()
        
        # Use WebDriverWait to wait for the button to be clickable
        # manually_input_btn = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
        # )

        # manually_input_btn = driver.find_element(By.CSS_SELECTOR, css_selector)
        # manually_input_btn.click()
        # Wait for the next page to load
        time.sleep(5)

        # #pickere9ce05bd > div > div
        download = "body > div:nth-child(2) > div.d-block.px-1.mx-1.my-1 > div > div > div > div:nth-child(4) > button"
        download_btn = driver.find_element(By.CSS_SELECTOR, download)
        download_btn.click()
        # Wait for the next page to load
        time.sleep(5)

        # Wait for download to complete (adjust time as necessary)
        timeout = time.time() + 60*5  # 5 minutes from now
        while True:
            if time.time() > timeout:
                print("Download timed out")
                break

            current_files = set(os.listdir(download_dir))
            new_files = current_files - existing_files
            print("Checking for new files...")

            for fname in new_files:
                if fname.endswith(".csv"):
                    print(f"New file downloaded: {fname}")
                    with open("downloaded_filename.txt", "w") as file:
                        file.write(fname)
                    # Exit the loop once the new file is found
                    return True
            time.sleep(1)
            
            # else:
            #     # Continue the loop if no new file is found
            #     time.sleep(1)
            #     continue

            # # Exit the loop once the new file is processed
            # break

    finally:
        # Close the browser
        driver.quit()
        print("Driver closed. Check for downloaded_filename.txt in the current working directory.")
    return False  # No new CSV file was downloaded


delete_existing_csv_files(download_dir)

while True:
    csv_files = [f for f in os.listdir(download_dir) if f.endswith('.csv')]
    if csv_files:
        print("CSV file(s) found in directory. No need to crawl again.")
        break
    else:
        print("No CSV file found. Start crawling...")
        if crawl_website(download_dir, driver_path):
            print("Crawl completed and found new CSV file.")
            break
        else:
            print("Crawl completed but no new CSV file found. Retrying...")