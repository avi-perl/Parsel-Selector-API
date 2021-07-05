# Parsel Selector API
An API for selecting part of a document on the web based on a path to the content. 
You can see a hosted version of the POC here: https://parsel-selector-api.herokuapp.com/docs

---
## Inspiration

The Python [Scrapy](https://scrapy.org/) project, a framework for web scraping, the [Parsel](https://pypi.org/project/parsel/) library is used to parse content scraped from the internet to get at the data the scraper wants. Getting page content looks something like this:
```python
>>> fetch("https://old.reddit.com/")
>>> response.xpath('//title/text()').get()
'reddit: the front page of the internet'
```

The above example is how a user might develop the correct xpath needed to get at the content they want, this typically involves a lot of trial and error. 

In [another project](https://html-notifier.herokuapp.com/explore/) I created a GUI to do this task within a browser which works quite nicely. The goal of this project is to create an API that does the same thing and more. 

This API serves 2 purposes.
1. An API that can back up a static website built as a static tool to assist Scrapy users.
2. A standalone API where a user can get specific page content with a path, a useful tool for all sorts of projects. 
---
## Features

- Parse HTML with Xpath or CSS selectors as you would in Scrapy/Parsel.
- Parse JSON and XML with a path similar to an Xpath.
- Parse any text content on the internet with a Regex pattern.
- Test out how the site you're working on reacts to different User-Agents.
- Built with Fast API which provides Swagger documentation.


---
## Whats Next?
This project is under development still, but the code as it stands is a working POC. Future plans include lots more documentation, tests perhaps, and a react frontend so this is useable from a GUI.