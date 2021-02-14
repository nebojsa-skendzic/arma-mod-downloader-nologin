import requests
import json
import time
import os

#https://steamcommunity.com/sharedfiles/filedetails/?id=2093224138


#you can also query when an item was last changed via steam web api
#POST https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/ with form body itemcount=1&publishedfileids[0]=$id

#you can fetch collection info via steam web api
#POST https://api.steampowered.com/ISteamRemoteStorage/GetCollectionDetails/v1/ with form body collectioncount=1&publishedfileids[0]=$id


def needsupdate(id, download_dir):

    url = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"

    data = requests.post(url, data = {"itemcount" : 1, "publishedfileids[0]" : id})
    data = json.loads(data.text)

    workshoptime = data['response']['publishedfiledetails'][0]['time_updated']

    modtime = os.path.getmtime(download_dir)

    if workshoptime > modtime:
        return True
    else:
        return False




