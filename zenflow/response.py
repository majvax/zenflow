from .const import STATUS_CODES, DEFAULT_HEADERS
from copy import deepcopy


class Response:
    def __init__(self, status_code: STATUS_CODES, headers: dict = None, body: str = "", http_version: str = "HTTP/1.1"):
        if headers is None:
            headers = deepcopy(DEFAULT_HEADERS)
        self.status_code = status_code
        self.headers = headers
        self.body = body
        self.http_version = http_version

    def __str__(self) -> str:
        string = f"{self.http_version} {self.status_code}\n{'\n'.join(f"{h}: {self.headers[h]}" for h in self.headers)}\n\n{self.body}"
        print(string)
        return string