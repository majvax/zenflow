import json as jsonlib



class Request:
    def __init__(self, request: str):
        self._header, self._url, self._method, self._version, self._body = self.parse_request(request)
        self._cookie
        try:
            self._json = jsonlib.loads(self._body)
        except Exception as _:
            self._json = jsonlib.loads("{}")


    @staticmethod
    def parse_request(request: str):
        lst = request.replace("\r", "").split('\n')
        print(lst)
        html = lst[0].split(' ')
        header = lst[1:]
        url = html[1]
        method = html[0]
        version = html[2]
        
        header = {i.split(": ")[0]: i.split(": ")[1] for i in header if i != "" and ": " in i}
        body = lst[-1] if "" in lst else ""

        return header, url, method, version, body
    
    @property
    def header(self) -> dict:
        return self._header
    
    @property
    def url(self) -> str:
        return self._url
    
    @property
    def method(self) -> str:
        return self._method
    
    @property
    def http_version(self) -> str:
        return self._version
    
    @property
    def body(self) -> str:
        return self._body

    @property
    def json(self) -> dict:
        return self._json


    def __repr__(self) -> str:
        return f"<Request {self.method} {self.url} {self.http_version}>"
    
    def __str__(self) -> str:
        return f"<Request {self.method} {self.url} {self.http_version}>"
    
    def __getitem__(self, key) -> str:
        return self.header[key]




