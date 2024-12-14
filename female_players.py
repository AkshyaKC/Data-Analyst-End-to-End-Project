import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Initialize the webdriver and open the page
driver = webdriver.Chrome()
base_url = "https://www.ea.com/games/ea-sports-fc/ratings?gender=1&page="
player_stat = []

def scrape_page(url):
    driver.get(url)
    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'Table_row__eoyUr')))

    # Find all the <tr> elements by class name
    trs = driver.find_elements(By.CLASS_NAME, 'Table_row__eoyUr')
    for tr in trs:
        tds = tr.find_elements(By.CLASS_NAME, 'Table_cell__qBFwB')
        if len(tds) >= 13:
            try:
                rank = int(tds[0].text)
                name = tr.find_element(By.XPATH, ".//td[2]//div[@class='Table_profileContent__Lna_E']").text
                row_data = [rank, name]

                # Append the row to the output list
                player_stat.append(row_data)
            except Exception as e:
                print("Error:", e)
    print(f"Page {page_number} is scraped")

# Filepath for the CSV
csv_file = 'female_players.csv'

# Loop through all pages
for page_number in range(1, 17):  # Adjust range for desired number of pages
    url = base_url + str(page_number)
    scrape_page(url)
    time.sleep(1)  # Sleep to avoid overwhelming the server

    # Convert collected data to DataFrame
    headers = ['rank', 'player_name']
    df_new = pd.DataFrame(player_stat, columns=headers)

    # Save the scraped data into the CSV
    if not os.path.exists(csv_file):
        # Create a new file if it doesn't exist
        df_new.to_csv(csv_file, index=False)
    else:
        # Append to the existing file
        df_new.to_csv(csv_file, mode='a', header=False, index=False)

    # Clear player_stat after saving
    player_stat = []

# Quit the driver
driver.quit()
