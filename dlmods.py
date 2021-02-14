from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
import subprocess
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import requests
import re
from pathlib import Path

def expand_shadow_element(element):
  shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
  return shadow_root

def enable_download_headless(browser,download_dir):
	browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
	params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
	browser.execute("send_command", params)

def steam_workshop_list(workshop_link, links_dict):
	data = requests.get(workshop_link)
	data = data.text
	soup = BeautifulSoup(data, 'html.parser')

	for div in soup.find_all('div', class_="collectionItemDetails"):
		i = 0
		for a in div.find_all('a', href = True):
			if i == 0:
				link = a['href']
				i = i + 1
			for d2 in a.find_all('div', class_="workshopItemTitle"):
				title = d2.text

		links_dict[title] = link

def downloader(it):
	global pathcreated
	global pathexist

	while True:

			# initialize an object to the location on the html page and click on it to download
			elem = driver.find_element_by_id("downloadUrlLabel")
			elem.click()
			elem.send_keys("https://steamcommunity.com/sharedfiles/filedetails/?id=")

			mod_id = value[value.index("=")+1:]
			for r in mod_id:
				elem.send_keys(r)
				time.sleep(0.1)


			#Get the mod name on the steam downloader page for verification purposes, because it bugs out.
			try:
				mod_name = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='root']/main/div[3]/div/div/div/div/div[1]/div[2]/h6/a")))
				mod_name = mod_name.text
			except:
				continue

			#setting a separate download folder on each occasion - HAS TO STAY HERE BECAUSE DOWNLOAD WON'T START WITHOUT THE DIRECTORY BEING MADE ALREADY


			try:
				dlbutton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "align-self-end")))
				if dlbutton.text == "Download" and key == mod_name:
					Path(download_dir).mkdir(parents=True, exist_ok=True)
					pathcreated = True
					time.sleep(1)
					dlbutton.click()
					break
				else:
					print ("Mod names don't match, trying again. \n")
					elem.clear()
					time.sleep(1)
					it = it + 1
					if it > 6:
						if input("The name of the mod on steam downloader is {}. The mod that should be downloaded is {}. Continue? Y/N? ".format(mod_name, key)).lower() == "y":
							Path(download_dir).mkdir(parents=True, exist_ok=True)
							pathcreated = True
							time.sleep(1)
							dlbutton.click()
							break
						else:
							driver.get("https://steamworkshopdownloader.io/")
							continue
					elif it % 2 == 0:
						driver.get("https://steamworkshopdownloader.io/")
						continue
			except:
				elem.clear()
				continue


# instantiate a chrome options object so you can set the size and headless preference
options = Options()
options.add_argument("--headless")
#chrome_options.binary_location = "C:/Program Files/Google/Chrome Beta/Application/chrome.exe"
options.add_argument("--window-size=1920x1080")
options.add_argument("--disable-notifications")
options.add_argument('--no-sandbox')
options.add_argument('--verbose')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option("prefs", {
		"download.prompt_for_download": False,
		"download.directory_upgrade": True,
		"safebrowsing_for_trusted_sources_enabled": False,
		"safebrowsing.enabled": False
})
options.add_argument('--disable-gpu')
options.add_argument('--disable-software-rasterizer')

# initialize driver object and change the <path_to_chrome_driver> depending on your directory where your chromedriver should be
driver = webdriver.Chrome(options=options, executable_path=r"{}".format(input("Insert path to chromedriver, inclucing filename ex: /home/user/chromedriver. \n")))

mods_main_folder = r"{}".format(input("Enter path to mods directory: \n"))
islinux = input("Are you on linux? Y/N ").lower()
#Get the collection link and get all mod names + workshop links
linksnames = {}
steam_workshop_list(input("Enter workshop link: \n"), linksnames)
for_progress_tracking = list(linksnames.values())



for key, value in linksnames.items():

	# get request to target the site selenium is active on
	driver.get("https://steamworkshopdownloader.io/")

	replace_list=["\'", "[", "]", "(", ")", ".", ":", ","]
	mod_dir = re.sub('\s+', '', key)
	mod_dir = mod_dir.lower()
	for i in replace_list:
		mod_dir = mod_dir.replace(i, "")

	if islinux == 'y':
		download_dir = r"{}".format(mods_main_folder + "/@" + mod_dir)
	else:
		download_dir = r"{}".format(mods_main_folder + "\@" + mod_dir)
	enable_download_headless(driver, download_dir)

	pathexist = os.path.exists(download_dir)#These two check if folder doesn't exist and downloads the mods. Once it's created it pathcreated = true and pathexists = False meaning it has just been created and the downloading should continue
	pathcreated = False

	it = 0
	if not pathexist:
		downloader(it)
		pass
	else:
		print("Mod folder for {} already exists. Skipping...\n".format(key))
		time.sleep(1)

	if not pathexist and pathcreated:
		downloading = True
		dlmsg = False
		iter = 0
		while downloading:
			if iter > 60:
				  it = 0
				  downloader(it)
				  iter = 0
			for fname in os.listdir(download_dir):
				if fname.endswith('.zip') or fname.endswith('.rar'):
					downloading = False
					print ("Download complete for: {}\n".format(key))
				elif fname.endswith('.crdownload') and not dlmsg:
					print(("Download started for {}\n").format(key))
					dlmsg = True
					downloading = True
					iter = iter + 1
					time.sleep(1)
				else:
					downloading = True
					iter = iter + 1
					time.sleep(1)

		time.sleep(1)

		if islinux == 'y':
			toextract = os.listdir(download_dir)
			os.chdir(download_dir)
			if len(toextract) == 1:
				subprocess.run(["unzip", toextract[0]])
				subprocess.run(["rm", "-r", toextract[0]])

	print ("Downloaded {} of {} mods..\n \n".format(for_progress_tracking.index(value)+1, len(linksnames)))


