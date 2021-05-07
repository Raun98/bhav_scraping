# Bhav Scraper Website
An easy to use website to scrape information from www.bseindia.com/ and collect BhavCopy from it.

# Basic Requirements:

Python Django web app/server that:

- Downloads the equity bhavcopy zip from [here](https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx) every day at 18:00 IST for the current date.
- Extracts and parses the CSV file in it.
- Writes the records into Redis with appropriate data structures (Fields: code, name, open, high, low, close).
- Renders a simple VueJS frontend with a search box that allows the stored entries to be searched by name and renders a table of results and optionally downloads the results as CSV. Make this page look nice!
- The search needs to be performed on the backend using Redis.

# Setup Guide:

- Start by cloning this project to your computer.
- Install virtualenv using : `pip install virtualenv`
- Create a virtual environment using : `virtualenv -p python3 env .` 
- Create an src folder and extract the files to this directory. This will serve as the root directory.
- Install dependencies using `pip install -r requirements.txt` in your terminal.

# Running the web app
On 3 separate terminals, navigate to the env directory and activate the Virtual environment using  `.\Scripts\activate` on all 3 prompts.
Now, parallelly run each command in an individual terminal :
- `celery -A zda worker -l info -P gevent`
- `celery -A zda beat -l info`
- `python manage.py runserver`

Once setup is complete, a link to the webapp based on your local host will appear.
Django returns a URL to your local host, follow that to find the dashboard.

Thank you for reading! :book: :heart:
