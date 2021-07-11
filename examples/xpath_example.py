import requests

params = {
    "url": "http://127.0.0.1:8000/examples/xml",
    "path": "/note/to",
    "path_type": "XML",
}

# # Example using BASIC return style
# params["return_style"] = "BASIC"
# r = requests.get("https://parsel-selector-api.herokuapp.com/", params=params)
# print(r.json(), "\n")

# Example using DATA_ONLY return style
params["return_style"] = "DATA_ONLY"
r = requests.get("http://127.0.0.1:8000/", params=params)
print(r.text, "\n")

# # Example using VERBOSE return style
# params["return_style"] = "VERBOSE"
# r = requests.get("https://parsel-selector-api.herokuapp.com/", params=params)
# print(r.json(), "\n")

