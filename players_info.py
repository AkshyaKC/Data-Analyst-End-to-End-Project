from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

driver = webdriver.Chrome()
base_url = "https://www.ea.com/games/ea-sports-fc/ratings?page="

# Check if the CSV file exists; if not, create it with headers
file_name = 'players_info.csv'
if not os.path.exists(file_name):
    pd.DataFrame(columns=['player_name', 'age', 'league', 'preffered_foot', 'height_(in cm)', 'weight_(in kg)', 'alt_position']).to_csv(file_name, index=False)

def visit_player_profile(player_url):
    driver.get(player_url)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'AthletePage_playerNameMobile__ZBzlB')))
        player_name_div = driver.find_element(By.CLASS_NAME, 'AthletePage_playerNameMobile__ZBzlB')
        span_elements = player_name_div.find_elements(By.TAG_NAME, 'span')
        player_name = ' '.join(span.text for span in span_elements)
    except Exception as e:
        print(f"Error visiting {player_url}: {e}")
        return
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ItemGrid_grid__DKaHT')))
        div_grid_elements = driver.find_elements(By.CLASS_NAME, 'ItemGrid_grid__DKaHT')
        
        if len(div_grid_elements) >= 3:
            first_grid_div = div_grid_elements[0]
            preferred_foot = first_grid_div.find_element(By.XPATH, ".//div[text()='Preferred Foot']/following-sibling::span").text
            height = first_grid_div.find_element(By.XPATH, ".//div[text()='Height']/following-sibling::span").text.split('cm')[0].strip()
            weight = first_grid_div.find_element(By.XPATH, ".//div[text()='Weight']/following-sibling::span").text.split('kg')[0].strip()
            alt_positions_divs = first_grid_div.find_elements(By.XPATH, ".//div[text()='Alt Positions']/following-sibling::div//div[@class='Tag_tagInner__1n1uo']")
            alt_positions = [div.text for div in alt_positions_divs] if alt_positions_divs else None
            
            third_grid_div = div_grid_elements[2]
            age = third_grid_div.find_element(By.XPATH, ".//div[text()='Age']/following-sibling::span").text
            league = third_grid_div.find_element(By.XPATH, ".//div[text()='League']/following-sibling::span").text

            # Save the row directly into the CSV
            player_data = {'Player Name': player_name, 'Age': age, 'League': league, 'Preferred Foot': preferred_foot, 'Height (in cm)': height, 'Weight (in kg)': weight, 'Alt Position': alt_positions}
            pd.DataFrame([player_data]).to_csv(file_name, mode='a', header=False, index=False)

    except Exception as e:
        print(f"Could not find the necessary elements for player: {player_name}, Error: {e}")

def scrape_page(url):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'Table_row__eoyUr')))
    
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    trs = soup.find_all('tr', class_='Table_row__eoyUr')
    
    for tr in trs:
        anchor_tag = tr.find('a', class_='Table_profileCellAnchor__L23hq')
        player_url = 'https://www.ea.com' + anchor_tag['href'] if anchor_tag else None
        
        if player_url:
            visit_player_profile(player_url)

# Loop through all pages and scrape
for page_number in range(113, 176):
    url = base_url + str(page_number)
    scrape_page(url)
    print(f"Page {page_number} is scrapped")
    time.sleep(1)

driver.quit()