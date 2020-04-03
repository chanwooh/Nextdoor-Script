# Nextdoor Scraper

At the time of development, Nextdoor could not be scraped easily using more traditional methods (e.g. Scrapy, Beautiful Soup, etc.) because requests to retrieve the next set of posts use a "random" number as a parameter. 

Thus, this is a simple python script that uses Selenium to simulate user input to scrape relevant data off nextdoor.com. It uses a chromedriver (included in this repo) as the browser. 

## Requirements

As of the last update, this script will work with Python 3.8.0+. It is highly recommended a [virtual environment](https://github.com/pyenv/pyenv-virtualenv) is used for this script. 

Once a virtual environment is built, `pip install -r requirements.txt` must be run in a command prompt within the Nextdoor_Script directory to install relevant packages. The script will not work without these libraries.

## Using this Script

Feel free to fork this repo and make it your own! This was just a personal project of mine, but if it is useful to anyone else, I'm happy to share this project. If you'd like to use it as is:

1. Clone the repository into your directory of choosing.
2. Replace the \<Username\> and \<Password\> in `nextdoor.py`.
3. Open command prompt, navigate to the Nextdoor_Scraper directory, and run the script using `python nextdoor.py`

