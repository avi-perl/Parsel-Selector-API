import json

import dpath.util
import httpx
import asyncio
import xmltodict
from parsel import Selector

http_response_codes = {
    100: ("Continue", "Request received, please continue"),
    101: ("Switching Protocols", "Switching to new protocol; obey Upgrade header"),
    200: ("OK", "Request fulfilled, document follows"),
    201: ("Created", "Document created, URL follows"),
    202: ("Accepted", "Request accepted, processing continues off-line"),
    203: ("Non-Authoritative Information", "Request fulfilled from cache"),
    204: ("No Content", "Request fulfilled, nothing follows"),
    205: ("Reset Content", "Clear input form for further input."),
    206: ("Partial Content", "Partial content follows."),
    300: ("Multiple Choices", "Object has several resources -- see URI list"),
    301: ("Moved Permanently", "Object moved permanently -- see URI list"),
    302: ("Found", "Object moved temporarily -- see URI list"),
    303: ("See Other", "Object moved -- see Method and URL list"),
    304: ("Not Modified", "Document has not changed since given time"),
    305: (
        "Use Proxy",
        "You must use proxy specified in Location to access this resource.",
    ),
    307: ("Temporary Redirect", "Object moved temporarily -- see URI list"),
    400: ("Bad Request", "Bad request syntax or unsupported method"),
    401: ("Unauthorized", "No permission -- see authorization schemes"),
    402: ("Payment Required", "No payment -- see charging schemes"),
    403: ("Forbidden", "Request forbidden -- authorization will not help"),
    404: ("Not Found", "Nothing matches the given URI"),
    405: ("Method Not Allowed", "Specified method is invalid for this server."),
    406: ("Not Acceptable", "URI not available in preferred format."),
    407: (
        "Proxy Authentication Required",
        "You must authenticate with this proxy before proceeding.",
    ),
    408: ("Request Timeout", "Request timed out; try again later."),
    409: ("Conflict", "Request conflict."),
    410: ("Gone", "URI no longer exists and has been permanently removed."),
    411: ("Length Required", "Client must specify Content-Length."),
    412: ("Precondition Failed", "Precondition in headers is false."),
    413: ("Request Entity Too Large", "Entity is too large."),
    414: ("Request-URI Too Long", "URI is too long."),
    415: ("Unsupported Media Type", "Entity body in unsupported format."),
    416: ("Requested Range Not Satisfiable", "Cannot satisfy request range."),
    417: ("Expectation Failed", "Expect condition could not be satisfied."),
    500: ("Internal Server Error", "Server got itself in trouble"),
    501: ("Not Implemented", "Server does not support this operation"),
    502: ("Bad Gateway", "Invalid responses from another server/proxy."),
    503: (
        "Service Unavailable",
        "The server cannot process the request due to a high load",
    ),
    504: ("Gateway Timeout", "The gateway server did not receive a timely response"),
    505: ("HTTP Version Not Supported", "Cannot fulfill request."),
}

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
]


class ParselSelectorRetriever:
    XPATH = "XPATH"
    CSS = "CSS"
    REGEX = "REGEX"
    JSON = "JSON"
    XML = "XML"

    request = None
    path_data = None
    raw_path_data = None
    __url_response = None
    scrape_log = None
    error_code = None
    error_msg = None
    content_reformatted = False

    def __init__(
        self,
        url,
        path,
        path_type,
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    ):
        self.__url = url
        self.path = path
        self.path_type = path_type
        self.user_agent = user_agent

    async def run(self):
        """Makes the get request for the requested data"""
        async with httpx.AsyncClient() as client:
            make_request = self.request(client)
            self.request = await asyncio.gather(make_request)
            self.request = self.request[0]

            # Extract the data using the path provided
            self.path_data = self.raw_path_data = self._get_path_data()

            # Reformat data when the data should be represented as JSON
            if self.path_type in [self.JSON, self.XML, self.REGEX]:
                self.content_reformatted = True
                self.path_data = json.dumps(self.path_data, indent=2)

    async def request(self, client):
        response = await client.get(
            self.url,
            headers={"User-Agent": self.user_agent},
        )
        return response

    @property
    def url(self):
        """Sanitized and reformatted url"""
        url = self.__url if self.__url[:4].lower() == "http" else "http://" + self.__url
        return url

    @property
    def raw_data(self):
        """Returns the raw data that we got back from the request"""
        return self.request.content.decode('utf-8')

    @property
    def status_code(self):
        """Returns the status code from the request"""
        return self.request.status_code

    @property
    def status_msg(self):
        """Returns information about the response code from the request"""
        return http_response_codes.get(self.status_code)

    def _get_path_data(self):
        """Gets the path content based on the type of path that was requested"""
        data = None
        try:
            selector = Selector(text=self.raw_data)
            if self.path_type == self.XPATH:
                data = selector.xpath(self.path).get()
            elif self.path_type == self.CSS:
                data = selector.css(self.path).get()
            elif self.path_type == self.REGEX:
                data = selector.re(self.path)
            elif self.path_type == self.JSON:
                json_dict = json.loads(
                    self.full_response
                )  # Convert JSON to python dictionary
                data = dpath.util.get(
                    json_dict, self.path
                )  # Get the content of the dictionary based on the path provided
            elif self.path_type == self.XML:
                # Convert the xml into a valid python dictionary so we can parse it the same way we parse JSON
                try:
                    xml_dict = json.loads(
                        json.dumps(xmltodict.parse(self.full_response))
                    )
                except Exception:
                    self.error_code = 3
                    self.error_msg = (
                        "Error parsing XML data. Are you sure the data is valid XML?"
                    )
                    return data
                data = dpath.util.get(xml_dict, self.path)
        except KeyError:
            self.error_code = 1
            self.error_msg = f"Path error, please enter a valid Path value for the type '{self.path_type_name}'"
        except Exception as e:
            self.error_code = 2
            self.error_msg = (
                f"There was an error with your Path and Path Type combo: {e}"
            )
        return data

    @classmethod
    def from_selector_item(cls, selector_item):
        return cls(
            url=selector_item.url,
            path=selector_item.path,
            path_type=selector_item.path_type,
            user_agent=selector_item.user_agent,
        )
