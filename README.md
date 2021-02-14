
 <h3 align="center">Arma 3 Mod downloader - no login required</h3>

<p align="center">
    Use this tool to download mods for Arma 3 from the workshop without any login required. Originally developed to easily download or update mods for my A3 Linux server but can also be used on Windows with slightly more limited functionality.
<br />

## Features
* Download mods from the workshop (developed for Arma 3 but should work for any workshop colletion)
* Create lowercase and no whitespace mod folders (for Linux compatibility)
* Linux only: Extract the mods and remove the zip files
* Mod updating

### Prerequisites

* Execute the command:
  ```sh
  pip install -r requirements.txt
  ```

* Download the chromedriver for your system from [here](https://chromedriver.chromium.org/downloads).
* Ensure a compatible Chrome browser is installed - same version as the chromedriver.

### Usage

* Run the script and when it requests the chromedriver point to it.

Windows:
```sh
C:\Users\username\Desktop\arma-mod-downloader-nologin\chromedriver.exe
```

Linux:
```sh
/home/user/arma-mod-downloader-nologin/chromedriver
```

* Point it to the desired mods directory in a similar fashion.

* Paste the Steam Workshop collection link when requested.

Note: Linux functionality is expanded for now in that it will unzip the mod and remove the .zip file from the mod directory. For server owners, moving keys is not yet implemented. For Linux users, mod folder names are lowercase but files inside are not. Run the tolower.sh script from LinuxGSM.


### Updating

* Updating is done by deleting the mod folder of the mod you with to update and then running the script again as per above. It will skip all folders it finds and only download the missing ones.

### Known bugs:

* If the download is interrupted when running the script again it will skip over the mod that the download was interrupted on. This is because it checks for the presence of the mod folder, which was created in the previous run. This mod folder will be empty and must be removed before running the script again.

* In rare cases the downloader will fail to download a mod outright, in which case remove the newly created and empty mod folder and re-run the script.

### Built With

* Python 3
* BeautifulSoup
* Selenium

<a href="https://github.com/nebojsa-skendzic/arma-mod-downloader-nologin/issues">Report Bug</a>

Project Link: [https://github.com/nebojsa-skendzic/arma-mod-downloader-nologin](https://github.com/nebojsa-skendzic/arma-mod-downloader-nologin)


## License

Distributed under the MIT License. See `LICENSE` for more information.

