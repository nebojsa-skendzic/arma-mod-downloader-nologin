<h2>Deprecated. steamworkshopdownloader.io has been shut down</h2>
 <h3 align="center">Arma 3 Mod downloader - no login required</h3>

<p align="center">
    Use this tool to download mods for Arma 3 from the workshop without any login required. Originally developed to easily download or update mods for my A3 Linux server but can also be used on Windows with slightly more limited functionality.
<br />


## Features
* Download mods from the workshop (developed for Arma 3 but should work for any workshop colletion)
* Create lowercase and no whitespace mod folders (for Linux compatibility)
* Extract the mods and remove the zip files
* Mod updating

### Prerequisites

* Execute the command:
  ```sh
  pip install -r requirements.txt
  ```

### Usage

* Point it to the desired mods directory.

* Paste the Steam Workshop collection link when requested.

* Thanks to [ASDFGamer](https://github.com/ASDFGamer) you can start the script from the commandline with 2 arguments. The first one being mod location, the second one being the workshop collection link.

Note: Linux functionality is expanded for now in that it will unzip the mod and remove the .zip file from the mod directory. For server owners, moving keys is not yet implemented. For Linux users, mod folder names are lowercase but files inside are not. Run the tolower.sh script from LinuxGSM.


### Updating

* Updating will be done automatically upon running the script by checking the date the mod folder was last modified against the last update of the mod.

* Manual updating is done by deleting the mod folder of the mod you with to update and then running the script again as per above. It will skip all folders it finds and only download the missing ones.

### Known issues:

* The script may repeat the line "retrieving" on a single mod for a while. This is as intended and will be fixed. It means it's caching the mod from Steam servers. This take particularly long for big mods.

* Sometimes it may take a while for the download to finish in which case the script appears as stopped. Just leave it be until it completes the download.

### Built With

* Uses steamworkshopdownloader.io api
* Python 3
* BeautifulSoup
* Requests

<a href="https://github.com/nebojsa-skendzic/arma-mod-downloader-nologin/issues">Report Bug</a>

Project Link: [https://github.com/nebojsa-skendzic/arma-mod-downloader-nologin](https://github.com/nebojsa-skendzic/arma-mod-downloader-nologin)


## License

Distributed under the MIT License. See `LICENSE` for more information.
