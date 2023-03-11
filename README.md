# Artstation Search Scraper

# About
Many other scrapers for art station either are limited by username or trending feed, this one bypasses the cloudflare protection by opening a selenium window and then grabs the high res images of each item. Used personally for screensaver purposes. You can select the amount of images to download from the query, up to 100 currently, and they download locally to your specified folder then also upload to a google photos album.

## Installation

Clone this repo and use the modules directly (not recommended).

Clone this repo and run setup.py

## Set up authorization

Browse through [Google's authorization guide](https://developers.google.com/photos/library/guides/get-started#configure-app)

Quick recap:

Go to [Google Cloud Console](https://console.cloud.google.com).
Set up a new project, then on the menu select: `Api & Services` > `Library`.
In the library, search for "photos", select `Photo Library API` and click on the `ENABLE` button.
On the `API & Services, Photo Library API` select `Credentials`, and select the `+CREDENTIALS` and select in the dropdown `OAuth client ID`. Select the type of app to be created (for desktop application select "other") and give it a name. If you are an occasional user, you should before this thing select the authorization display (`OAuth Consent Screen`), and make it public (if you are not a g-Suite user \$\$\$. THe interface prompts you already to do so, if never done before).
After this, coming back to the main interface, select in the row of the OAuth 2.0 Client ID just created the download button (rightmost one). Download the `.json` file in the root of the project, and give it a meaningful name (because it must be used afterwards). Remember to keep all these secret files far from git pushes, so if you are committing your porject to a repository, add the downloaded file to the _.gitignore_.

Once run the authentication it should open a browser to authenticate.
If you are creating a project for non commercial use you need not apply for review, but you have to allow it, because Google show a big message of warining. Clicking on advanced, it shows the button to allow the authorization, even though the app is not reviewed by Google (useful for tests and personal use projects). A .token file will keep the authorization for further use

# Usage
Run app.py and input your desired values into the entry boxes, click scrape and wait for it to complete.

## License

MIT, see the _LICENSE_ file.
