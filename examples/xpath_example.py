import requests

params = {
    "url": "https://parsel-selector-api.herokuapp.com/examples/html",
    "path": "/html/body/div/span[3]/text()",
    "path_type": "XPATH",
}

# Example using BASIC return style
params["return_style"] = "BASIC"
r = requests.get("https://parsel-selector-api.herokuapp.com/", params=params)
print(r.json(), "\n")

# Example using DATA_ONLY return style
params["return_style"] = "DATA_ONLY"
r = requests.get("https://parsel-selector-api.herokuapp.com/", params=params)
print(r.text, "\n")

# Example using VERBOSE return style
params["return_style"] = "VERBOSE"
r = requests.get("https://parsel-selector-api.herokuapp.com/", params=params)
print(r.json(), "\n")

