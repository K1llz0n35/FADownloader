# FurAffinity Downloader

Hi there. I got tired of many FA downloaders not downloading the scraps or favorites and almost none of them would save tags, So here is this. It is a very simple to use and only requires Python and a few modules.


# Setup

Before running for the first time, there are a few things to do first. Start by downloading the latest version of Python ([Python 3.13.1](https://www.python.org/downloads/release/python-3131/)). Once it is finished installing, open Bash or Command Prompt and run the following command (All this does is download the required modules):`pip install beautifulsoup4 requests wget urllib3`. In the config.ini file, change the download_path to where you would like the files to be downloaded. After that, the only things left are to setup your account and pick what you want to download.
### For most browsers (Chrome, Edge, and Firefox)
 - Go to [FurAffinity](furaffinity.net) and login to your account. 
 - On the home page, press F12 or right click and inspect. In the menu that just opened, click the network tab at the top and press Ctrl+R. 

 ![Chrome Inspect Element](images%5Cinspect.png)
 
 - Once the page has reloaded scroll to the top of that menu and click on `www.furaffinity.net`. Once that has opened, navigate to the cookies tab, find the 'a' and 'b' cookies and copy their value into the config.ini file (You can edit it using any text editor).

Finally for the fun part, what you want to download. I've kept this as simple as I could make it. The downloader can download 4 main categories: Galleries, Favorites, Scraps, and Keyword Searches.

 - For Keyword Searches, it is as simple as taking what you would search on FA and putting it on a new line in the tags.txt file.
 - For Galleries and Favorites, just put the username of the user into a new line in the gallery.txt and favorites.txt files respectively. Please make sure to use the user's system side username. The quickest way to find this is just to go to their profile and grab it from the URL (For example: https://www.furaffinity.net/user/foxinuhhbox/ would be foxinuhhbox in the text file).
- For Scraps, it is the same as the Gallery, just make sure to change in the config.ini file `scrap = false` to `scrap = true`.

# Using the program
Once all of the setup is completed, all that is needed to run the program is to just run the fa.py file.
The program will run on it's own, and will close once it is completed
## Tag Sidecars
Automatically, the program saves file sidecars with the file information. Currently it only contains the submission's tags, but I will update this soon to include the artist, upload date, date of download, submission, and the description, as well as the ability to disable the sidecars.
## The Files
Files and sidecars are downloaded to the same folder, I may add something in the future to allow for downloading to seperate folders.

Files are saved as their exact files from FA with no alterations. This allows for images (of course) but also music, stories, and Flash files.

Sidecars are saved as json files with the following layout:
```
{
    "title": "Belly of the Beast",
    "creator": "hdalby33",
    "tags": [
            "Callum",
        "Axton",
        "Dragon",
        "Tiger",
        "Weight",
        "Gain",
        "Belly",
        "Fat",
        "Fatfur",
        "Bulging",
        "Huge",
        "Smothering",
        "Soft",
        "Squishy",
        "Cute",
        "Hot",
        "Thighs",
        "Thick",
        "Heavy",
        "Round",
        "Moobs",
        "Annanutara",
        "NS22_Highwater",
        "Hdalby33"
            ]
}
```
The file name for these sidecars `id.json` where id is the submission id.

This layout is optimized for Hydrus, but if you would like layouts for any other program, feel free to reach out and let me know.

# Contact
Please feel free to reach out to [K1llz0n35@protonmail.com](mailto:K1llz0n35@protonmail.com) with any problems or suggestions.

Stay safe and enjoy!