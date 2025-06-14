from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select

import csv
import os
import maskpass

addOptions = webdriver.ChromeOptions()
addOptions.add_argument("headless")

username = input("Enter username:")
password = maskpass.askpass()
verifyInput = 0
while verifyInput == 0:
        school = input("Which school are you assigning Chromecarts to?").upper()
        firstLetter = school[0]

        if firstLetter == "P":
                listWord = "PARKER"
                verifyInput = 1
        elif firstLetter == "E":
                listWord = "ELEM"
                verifyInput = 1
        else:
                print("""Invalid input. Please enter "p" for Parker, or "e" for Elementary.""")

directory = input("Enter the path to the folder with the Chromecart lists:")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=addOptions)



driver.get("IMSWebsite") #IMS Website goes here
driver.implicitly_wait(10)

driver.find_element(By.LINK_TEXT, "Legacy Early College - Parker").click()
driver.implicitly_wait(10)

driver.find_element(By.ID, "Login").click()
driver.implicitly_wait(10)

driver.find_element(By.ID, "ID_userLoginName").send_keys(username)
driver.find_element(By.ID, "ID_userLoginPassword").send_keys(password)
driver.find_element(By.NAME, "submit").click()
driver.implicitly_wait(10)

driver.find_element(By.ID, "TopLevelCatalog").click()
driver.implicitly_wait(10)

completedDevices = open("AssignedCarts.txt", "w")

for file in os.listdir(directory):
        filePath = os.path.join(directory, file)
        fileData = csv.reader(open(filePath))
        roomNum = f"{listWord} {file[:3]}"


        driver.find_element(By.ID, "Update Resources").click()
        driver.implicitly_wait(10)

        driver.find_element(By.ID, "batchUpdate").click()
        driver.implicitly_wait(10)


        driver.find_element(By.NAME, "changeLocation").click()
        location = Select(driver.find_element(By.ID, "location"))
        location.select_by_visible_text(roomNum)
        driver.find_element(By.ID, "buttonNext").click()
        driver.implicitly_wait(10)

        driver.find_element(By.XPATH, """//input[@type="file"]""").send_keys(filePath)
        driver.find_element(By.ID, "updateButton").click()
        driver.implicitly_wait(10)

        
        completedDevices.write(f"{file} \n")

driver.quit()