import time
import subprocess
import os
from bs4 import BeautifulSoup
import requests
import re
import json
from pathlib import Path
from shutil import rmtree, unpack_archive
import wget
import platform
import sys


def needsupdate(id, download_dir):

    url = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"

    data = requests.post(url, data={"itemcount": 1, "publishedfileids[0]": id})
    data = json.loads(data.text)

    try:
        workshoptime = data['response']['publishedfiledetails'][0]['time_updated']
    except Exception:
        workshoptime = 0

    try:
        modtime = os.path.getmtime(download_dir)
    except Exception:
        return True

    if workshoptime > modtime:
        return True
    else:
        return False


def getlinkdirect(id):

    def getstatus():
        global status
        status = requests.post(statusurl, json={"uuids": [data['uuid']]})
        status = status.json()

    # TODO Add switcher to second backend
    statusurl = "https://backend-01-prd.steamworkshopdownloader.io/api/download/status"
    urlreq = "https://backend-01-prd.steamworkshopdownloader.io/api/download/request"
    urldl = "https://backend-01-prd.steamworkshopdownloader.io/api/download/transmit?uuid="

    data = requests.post(urlreq, json={"publishedFileId": int(id)})
    data = json.loads(data.text)
    link = urldl + data['uuid']

    getstatus()

    while status[data['uuid']]['status'] != "prepared":
        getstatus()
        try:
            print(status[data['uuid']]['status'])
            time.sleep(3)
        except Exception as e:
            print(e)
            time.sleep(3)
            continue
    print("Downloading...")
    return link


def steam_workshop_list(workshop_link, links_dict):
    data = requests.get(workshop_link)
    data = data.text
    soup = BeautifulSoup(data, 'html.parser')

    for div in soup.find_all('div', class_="collectionItemDetails"):
        i = 0
        for a in div.find_all('a', href=True):
            if i == 0:
                link = a['href']
                i = i + 1
            for d2 in a.find_all('div', class_="workshopItemTitle"):
                title = d2.text

        links_dict[title] = link


def downloader():
    global pathcreated

    while True:
        Path(download_dir).mkdir(parents=True, exist_ok=True)
        pathcreated = True
        time.sleep(1)
        print("Starting download for {} \n".format(key))
        try:
            wget.download(getlinkdirect(modid), download_dir)
            break
        except Exception:
            print("Retrying... \n")
            continue


linksnames = {}
if platform.system() == "Linux":
    islinux = True
else:
    islinux = False

if (len(sys.argv) == 3):
    mods_main_folder = sys.argv[1]
    steam_workshop_list(sys.argv[2],linksnames)
elif (len(sys.argv) == 1):
    mods_main_folder = r"{}".format(input("Enter path to mods directory: \n"))
    # Get the collection link and get all mod names + workshop links
    steam_workshop_list(input("Enter workshop link: \n"), linksnames)
else:
    print("Usage:")
    print("This program takes two arguments: the path to the mod folder and the link to the steam collection.")
    print("If no arguments are given the two arguments are asked in an interactive manner.")
    exit()
for_progress_tracking = list(linksnames.values())


for key, value in linksnames.items():
    modid = value[value.index("=") + 1:]
    replace_list = ["\'", "[", "]", "(", ")", ".", ":", ",", "|"]
    mod_dir = re.sub('\s+', '', key)
    mod_dir = mod_dir.lower()
    for i in replace_list:
        mod_dir = mod_dir.replace(i, "")

    if islinux:
        download_dir = r"{}".format(mods_main_folder + "/@" + mod_dir)
    else:
        download_dir = r"{}".format(mods_main_folder + "\@" + mod_dir)

    isemptyfolder = False
    try:
        if len(os.listdir(download_dir)) < 1:
            isemptyfolder = True
    except Exception:
        pass

    # These two check if folder doesn't exist or if
    # an update has been released and downloads the mods.
    if (os.path.exists(download_dir)) and not isemptyfolder:
        modupdate = needsupdate(modid, download_dir)
        if modupdate:
            rmtree(download_dir)
    elif isemptyfolder:
        modupdate = True
    else:
        modupdate = True
    pathcreated = False

    if modupdate:
        downloader()
        pass
    elif not modupdate:
        print("Mod {} doesn't require an update. Skipping...".format(key))
        time.sleep(1)
    else:
        print("Mod folder for {} already exists. \
            Skipping, but this message shouldn't appear. \
            Consider restarting the script.\n".format(key))
        time.sleep(1)

    if pathcreated and modupdate:
        downloading = True
        while downloading:
            for fname in os.listdir(download_dir):
                if fname.endswith('.zip') or fname.endswith('.rar'):
                    downloading = False
                    print("Download complete for: {}\n".format(key))
                else:
                    downloading = True
                    time.sleep(1)

        time.sleep(1)

        if islinux:
            toextract = os.listdir(download_dir)
            os.chdir(download_dir)
            if len(toextract) == 1:
                subprocess.run(["unzip", toextract[0]])
                subprocess.run(["rm", "-r", toextract[0]])
        else:
            for fname in os.listdir(download_dir):
                if fname.endswith('.zip'):
                    format = "zip"
                    filename = fname
                elif fname.endswith('.rar'):
                    format = "rar"
                    filename = fname
            archivepath = download_dir + "\\" + filename
            unpack_archive(archivepath, download_dir, format)
            os.remove(archivepath)

    print("\n Downloaded {} of {} mods..\n \n".format
          (for_progress_tracking.index(value) + 1, len(linksnames)))
