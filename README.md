# Nextdoor Scraper

At the time of website or software development, Nextdoor could not be scraped easily using more traditional methods like Scrapy, Beautiful Soup etc. because requests to retrieve the next set of posts use a "random" number as a parameter. 

Thus, this is a simple python script that uses Selenium to simulate user input to scrape relevant data off nextdoor.com. It uses a chromedriver (included in this repo) as the browser. 

## Requirements

As of the last update, this script will work with Python 3.8.0+. It is highly recommended a [virtual environment](https://github.com/pyenv/pyenv-virtualenv) is used for this script. 

Once a virtual environment is built, `pip install -r requirements.txt` must be run in a command prompt within the Nextdoor_Script directory to install relevant packages. The script will not work without these libraries.

## Using this Script

Feel free to fork this repo and make it your own! This was just a personal project of mine, but if it is useful to anyone else, I'm happy to share this project. If you'd like to use it as is:

1. Clone the repository into your directory of choosing.
2. Create your own enviroment `.env` file, and fill out the variables
3. Open command prompt, navigate to the Nextdoor_Scraper directory, and run commands mentioned bellow:
	* `python nextdoor.py` if you don't want to save the html file separately (as backup in case of failure)
	* `python html_saver.py` if you want to save the html files and `python html_scraper.py` to scrape the local files separately (more stable for longer scrapes since it'll save the files)

