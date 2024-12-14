import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Initialize the webdriver and open the page
driver = webdriver.Chrome()
base_url = "https://www.ea.com/games/ea-sports-fc/ratings?page="
player_stat = []

def scrape_page(url):
    driver.get(url)
    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'Table_row__4INyY')))

    # Find all the <tr> elements by class name
    trs = driver.find_elements(By.CLASS_NAME, 'Table_row__eoyUr')
    for tr in trs:
        tds = tr.find_elements(By.CLASS_NAME, 'Table_cell__qBFwB')
        if len(tds) >= 13:
            try:
                rank = int(tds[0].text)
                name = tr.find_element(By.XPATH, ".//td[2]//div[@class='Table_profileContent__Lna_E']").text
                image_url = tr.find_element(By.XPATH, ".//td[2]//div[contains(@class, 'Table_profileImageForeground__aWIxV')]//img").get_attribute('src')
                nationality = tr.find_element(By.XPATH, ".//td[3]//img").get_attribute('alt')
                club = tr.find_element(By.XPATH, ".//td[4]//img").get_attribute('alt')
                position = tr.find_element(By.XPATH, ".//td[5]//span").text

                # Get players' ratings
                last_td = tr.find_element(By.CLASS_NAME, 'Table_rowBlock__Ym9Qr')
                ovr = last_td.find_element(By.XPATH, ".//table//tbody//tr[1]//span[@class='Table_statCellValue__0G9QI']").text
                row_data = [rank, name, image_url, nationality, club, position, ovr]

                stat_tr = last_td.find_element(By.CLASS_NAME, "Table_rowBlockGroup__NbncE")
                if stat_tr:
                    stat_tds = stat_tr.find_elements(By.CLASS_NAME, "Table_cell__JtoBX")
                    for td in stat_tds:
                        try:
                            main_span = td.find_element(By.XPATH, ".//span[@class='Table_statCellValue__0G9QI']")
                            value = int(main_span.text.split("\n")[0])
                            try:
                                second_span = main_span.find_element(By.XPATH, ".//span")
                                class_name = second_span.get_attribute("class")
                                change_value = int(second_span.text)

                                if "Table_statChangeDecrease__9dvI1" in class_name:
                                    change_value = -abs(change_value)
                            except:
                                change_value = 0
                            row_data.extend([value, change_value])  # Add stats to the row
                        except:
                            row_data.extend(["No value", 0])  # Handle missing spans
                else:
                    row_data.extend(["No stats", 0])  # Handle missing stats block

                # Append the row to the output list
                player_stat.append(row_data)
            except Exception as e:
                print("Error:", e)
    print(f"Page {page_number} is scraped")

# Filepath for the CSV
csv_file = 'Fifa25.csv'

# Loop through all pages
for page_number in range(113, 176):  # Adjust range for desired number of pages
    url = base_url + str(page_number)
    scrape_page(url)
    time.sleep(1)  # Sleep to avoid overwhelming the server

    # Convert collected data to DataFrame
    headers = ['rank', 'player_name', 'image_url', 'nationality', 'club', 'position', 'ovr',
               'pac', 'pac+-', 'sho', 'sho+-', 'pas', 'pas+-', 'dri', 'dri+-', 'def', 'def+-', 'phy', 'phy+-']
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
