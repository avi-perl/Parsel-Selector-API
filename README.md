# Parsel Selector API
[![Python application](https://github.com/avrohom-perl/Parsel-Selector-API/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/avrohom-perl/Parsel-Selector-API/actions/workflows/python-app.yml) [![CodeQL](https://github.com/avrohom-perl/Parsel-Selector-API/actions/workflows/codeql-analysis.yml/badge.svg?branch=main)](https://github.com/avrohom-perl/Parsel-Selector-API/actions/workflows/codeql-analysis.yml)

An API for selecting part of a document on the web based on a path to the content.

- Swagger Documentation: https://parsel-selector-api.herokuapp.com/docs
- ReDoc Documentation: https://parsel-selector-api.herokuapp.com/redoc

---
## Quick Examples
Select these links for cool information about the world, powered by this API:
- [The number of humans currently in space](https://parsel-selector-api.herokuapp.com/dpath?url=https%3A%2F%2Fwww.howmanypeopleareinspacerightnow.com%2Fpeopleinspace.json&path=%2Fnumber&path_type=JSON&return_style=DATA_ONLY&user_agent=Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%3B%20rv%3A89.0%29%20Gecko%2F20100101%20Firefox%2F89.0) - [Source Data](https://www.howmanypeopleareinspacerightnow.com/peopleinspace.json)
- [Title of the current top post on all of Reddit](https://parsel-selector-api.herokuapp.com/parsel?url=https%3A%2F%2Fold.reddit.com%2Fr%2Fall%2F&path=%2Fhtml%2Fbody%2Fdiv%5B4%5D%2Fdiv%2Fdiv%5B1%5D%2Fdiv%5B2%5D%2Fdiv%5B1%5D%2Fp%5B1%5D%2Fa%2Ftext%28%29&path_type=XPATH&return_style=DATA_ONLY&user_agent=Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%3B%20rv%3A89.0%29%20Gecko%2F20100101%20Firefox%2F89.0) - [Source Data](https://old.reddit.com/r/all/)
- [Cover of Amazon's best selling book](https://parsel-selector-api.herokuapp.com/parsel?url=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fbestsellers%2Fbooks&path=%2Fhtml%2Fbody%2Fdiv%5B1%5D%2Fdiv%5B3%5D%2Fdiv%2Fdiv%2Fdiv%5B1%5D%2Fdiv%2Fol%2Fli%5B1%5D%2Fspan%2Fdiv%2Fspan%2Fa%2Fspan%2Fdiv%2Fimg&path_type=XPATH&return_style=DATA_ONLY&user_agent=Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%3B%20rv%3A89.0%29%20Gecko%2F20100101%20Firefox%2F89.0) - [Source Data](https://www.amazon.com/gp/bestsellers/books)

**How it works:** Users pass the API a url do a document on the web, and a path to particular content on that page. The page is scraped, and the data requested is returned!

---
## Inspiration

In the [Scrapy](https://scrapy.org/) python project, a framework for web scraping, the [Parsel](https://pypi.org/project/parsel/) library is used to parse content scraped from the internet to get at the data the scraper wants. Getting page content looks something like this:
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
- Caching functionality on unique url/user_agent combos when the requests status_code = 200, suppressing the API from calling an endpoint too frequently. 

## Installation
You can clone this repo for your own hosted version, or you can use the hosted version at https://parsel-selector-api.herokuapp.com/docs
```bash
# Clone repo
git clone https://github.com/avi-perl/Parsel-Selector-API.git
cd Parsel-Selector-API

# Install requirements 
pip install -r requirements.txt

# Run the app
uvicorn app.main:app --reload
```

## Usage 
Additional examples can be found in the examples folder.
```python
import requests

# Example using the default BASIC return style
params = {
    "url": "https://parsel-selector-api.herokuapp.com/examples/html",
    "path": "/html/body/div/span[3]/text()",
    "path_type": "XPATH"
}

r = requests.get("https://parsel-selector-api.herokuapp.com/parsel", params=params)
print(r.json())
```

### Parsing Content
Select the links below for documentation on how to structure your path for each type based on the library's used to power it.
| Type    | Library Used | Notes |
| ------- | ------------ | ----- |
| XPATH   | [Parsel](https://parsel.readthedocs.io/en/latest/usage.html#usage) | Currently only supporting the `.get()` method. |
| CSS     | [Parsel](https://parsel.readthedocs.io/en/latest/usage.html#usage) | Currently only supporting the `.get()` method. |
| REGEX   | [Parsel](https://parsel.readthedocs.io/en/latest/usage.html#usage) | 
| JSON    | [dpath](https://pypi.org/project/dpath/) | |
| XML     | XML converted to a dictionary by [xmltodict](https://pypi.org/project/xmltodict/), then parsed as JSON is with [dpath](https://pypi.org/project/dpath/) | |

## Contributing
This project has been mostly about learning, your pull requests and comments would be super appreciated! 

## TODO:
- [x] Add request cache so that the same URL is not called frequently.
- [ ] Add more tests on basic functionality.
- [ ] Create a front-end as a GUI for this tool.
- [ ] Add path parsing errors to the response for types other than XML.

## License
[MIT](https://choosealicense.com/licenses/mit/)