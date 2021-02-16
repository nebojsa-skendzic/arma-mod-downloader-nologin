import requests
import json
import time
import os


def needsupdate(id, download_dir):

    url = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"

    data = requests.post(url, data={"itemcount": 1, "publishedfileids[0]": id})
    data = json.loads(data.text)

    workshoptime = data['response']['publishedfiledetails'][0]['time_updated']

    try:
        modtime = os.path.getmtime(download_dir)
    except:
        return True

    if workshoptime > modtime:
        return True
    else:
        return False
