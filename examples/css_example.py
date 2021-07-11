import requests

# Example using BASIC return style
params = {
    "url": "https://parsel-selector-api.herokuapp.com/examples/html",
    "path": "body > h1",
    "path_type": "CSS",
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "return_style": "BASIC",
}
r = requests.get("https://parsel-selector-api.herokuapp.com/", params=params)
print(r.json())

# Example using DATA_ONLY return style
params = {
    "url": "https://parsel-selector-api.herokuapp.com/examples/html",
    "path": "body > h1",
    "path_type": "CSS",
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "return_style": "DATA_ONLY",
}
r = requests.get("https://parsel-selector-api.herokuapp.com/", params=params)
print(r.text)

# Example using VERBOSE return style
params = {
    "url": "https://parsel-selector-api.herokuapp.com/examples/html",
    "path": "body > h1",
    "path_type": "CSS",
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "return_style": "VERBOSE",
}
r = requests.get("https://parsel-selector-api.herokuapp.com/", params=params)
print(r.json())
