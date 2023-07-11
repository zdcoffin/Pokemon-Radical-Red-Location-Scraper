import csv
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC



url = "https://dex.radicalred.net/pokemon/"

driver = webdriver.Firefox()
driver.maximize_window()

driver.get(url)

names = wait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'col.pokemonnamecol')))

while True:

    driver.execute_script('arguments[0].scrollIntoView();', names[-1])

    try:
        wait(driver, 5).until(lambda driver: len(wait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'col.pokemonnamecol')))) > len(names))

        names = wait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'col.pokemonnamecol')))
    except:
        break

list_of_names = []

for name in names:
    list_of_names.append(name.get_attribute("innerText"))

with open("RR_names_list.txt", "w") as rr_names:
    
    for name in list_of_names:
        try:
            rr_names.write(name)
            rr_names.write("\n")
        except:
            rr_names.write(name[0])
            rr_names.write("\n")