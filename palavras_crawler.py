# -*- coding: utf-8 -*-
"""
Spyder Editor

Este é um arquivo de script temporário.
"""

# import os, time
#import complexidade_textual as ct
from selenium import webdriver
from selenium.webdriver.support.ui import Select


#files, paths = ct.corpus_reader("./corpora/Redações")

# Setting up Firefox

profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 1)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/html")
profile.update_preferences()


driver = webdriver.Firefox(profile)
driver.get("https://visl.sdu.dk/visl/pt/parsing/automatic/trees.php")
assert "VISL - Tree structure" in driver.title

#Textbox element that will receive the parsed text
text_box = driver.find_element_by_name("text")
text_box.clear()
text_box.send_keys("O texto que eu preciso parsear")

# Select vertical visualization from dropdown box
visualization = Select(driver.find_element_by_name('visual'))
visualization.select_by_visible_text("Vertical")

# Click to export html file with parsed structure
exp_down = driver.find_element_by_name("export")
exp_down.click()

#parsed_text = driver.find_element_by_css_selector("body > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > form:nth-child(3) > pre:nth-child(4)")

# time.sleep(5)

