# Parsel Selector API
An API for selecting part of a document on the web based on a path to the content.

- Swagger Documentation: https://parsel-selector-api.herokuapp.com/docs
- ReDoc Documentation: https://parsel-selector-api.herokuapp.com/redoc

## Inspiration

The Python [Scrapy](https://scrapy.org/) project, a framework for web scraping, the [Parsel](https://pypi.org/project/parsel/) library is used to parse content scraped from the internet to get at the data the scraper wants. Getting page content looks something like this:
```python
>>> fetch("https://old.reddit.com/")
>>> response.xpath('//title/text()').get()
'reddit: the front page of the internet'
```

The above example is how a developer might develop the correct xpath needed to get at the content they want, this typically involves a lot of trial and error. 

In [another project](https://html-notifier.herokuapp.com/explore/) I created a GUI to do this task within a browser which works quite nicely. The goal of this project is to create an API that does the same thing and more. 

This API serves 2 purposes.
1. A standalone API where a user can get specific page content with a path, a useful tool for all sorts of projects. 
2. An API that can back up a static website built as a static tool to assist Scrapy users.

## Features

- Parse HTML with Xpath or CSS selectors as you would in Scrapy/Parsel.
- Parse JSON and XML with a path similar to an Xpath.
- Parse any text content on the internet with a Regex pattern.
- Test out how the site you're working on reacts to different User-Agents.
- Built with Fast API which provides Swagger and ReDoc documentation.

## Installation
You can clone this repo for your own hosted version, or you can use the hosted version at https://parsel-selector-api.herokuapp.com/docs
```bash
# Clone repo
git clone https://github.com/avrohom-perl/Parsel-Selector-API.git
cd Parsel-Selector-API

# Install requirements 
pip install -r requirements.txt

# Run the app
uvicorn main:app --reload
```

## Usage 
Additional examples can be found in the examples folder.
```python
import requests

# Example using BASIC return style
params = {
    "url": "https://parsel-selector-api.herokuapp.com/examples/html",
    "path": "/html/body/h1/text()",
    "path_type": "XPATH",
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "return_style": "BASIC",
}

r = requests.get("https://parsel-selector-api.herokuapp.com/", params=params)
print(r.json())
```

## Contributing
Pull requests are welcome!

#### TODO:
- [ ] Add request cache so that the same URL is not called frequently.
- [ ] Add examples for each of the path types.
- [ ] Add tests.
- [ ] Create a front-end as a GUI for this tool.

## License
[MIT](https://choosealicense.com/licenses/mit/)