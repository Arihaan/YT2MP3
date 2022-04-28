# YT2MP3: YouTube to MP3 Downloader
A Python program which uses Selenium browser automation to download multiple MP3s at once from entered YouTube links.

<p align="center">
<img src="https://raw.githubusercontent.com/Arihaan/YT2MP3/main/Screenshot.png" width="900"></img>
</p>

## Installation

1. Open the YT2MP3 directory in any IDE.
2. You must have [Google Chrome](https://www.google.com/chrome/ "Chrome Link"), [Python 3](https://www.python.org/downloads/ "Python 3 link") and [pip](https://pypi.org/project/pip/ "PIP link") installed.
3. Install the required modules by running `pip install -r requirements.txt` on the Terminal.
4. Download the appropriate [chromedriver](https://chromedriver.chromium.org/downloads "chromedriver link") according to your version of Chrome. You can check the version by entering `chrome://version/` into Chrome's search bar. Replace the pre-existing chromedriver with the new one.
5. Run `YT2MP3.py`.

## Usage

Simply enter the URL of the video whose MP3 you'd like to download and click on "Add". The details of the video will then be displayed in the Console or an error will be thrown if the link is invalid. 

Once you've entered all the URLs, click on "Download All". This will then create a folder called "Downloaded MP3s" in the YT2MP3 directory and save all the MP3s there.

Please note that the program will freeze after clicking "Download All" depending on how many MP3s are being downloaded. Do not try to download an MP3 that already exists in the folder as that tends to break the program.

## License
[MIT](https://opensource.org/licenses/MIT "MIT Link")
