from functools import wraps
from typing import Literal
import socket
import re


REQUEST_TYPES = Literal['GET', 'POST', 'PUT', 'DELETE']

class Request:
    def __init__(self, request: str):
        self._header, self._url, self._type, self._version = self.parse_request(request)
        
    @staticmethod
    def parse_request(request: str):
        lst = request.replace("\r", "").split('\n')
        html = lst[0].split(' ')
        header = lst[1:]
        url = html[1]
        type = html[0]
        version = html[2]
        
        header = {i.split(": ")[0]: i.split(": ")[1] for i in header if i != "" and ": " in i}
        return header, url, type, version
    
    @property
    def header(self) -> dict:
        return self._header
    
    @property
    def url(self) -> str:
        return self._url
    
    @property
    def type(self) -> REQUEST_TYPES:
        return self._type
    
    @property
    def version(self) -> str:
        return self._version
    
    def __repr__(self) -> str:
        return f"<Request {self.type} {self.url} {self.version}>"
    
    def __str__(self) -> str:
        return f"<Request {self.type} {self.url} {self.version}>"
    
    def __getitem__(self, key) -> str:
        return self.header[key]
        

class Server:
    def __init__(self, host='127.0.0.1', port=8000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.running = True
        self.routes = {}

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        self.server_socket.settimeout(1)
        print(f"Server running on {self.host}:{self.port}")

        try:
            while self.running:
                try:
                    conn, addr = self.server_socket.accept()
                except socket.timeout:
                    continue

                with conn:
                    request = conn.recv(1024).decode('utf-8')
                    path = self.parse_request_path(request)
                    response = self.route_request(path)
                    test = Request(request)
                    print(test.type)
                    conn.sendall(response.encode('utf-8'))
        except KeyboardInterrupt:
            print("Keyboard Interrupt received, stopping server.")
        finally:
            self.stop()

    def parse_request_path(self, request):
        # Simple parsing to extract the path from the HTTP request
        try:
            return request.split(' ')[1]
        except IndexError:
            return '/'

    def route_request(self, path):
        # Match the paroutes = {}  # Global dictionary to store routes and their handlers

        for route, handler in self.routes.items():
            # check for arguments is route
            match = re.match(route, path)
            print(route, route, match)
            if match:
                args = match.group()
                return handler(*args)
            elif path == route:
                return handler()
        return "HTTP/1.1 404 Not Found\n\n404 Not Found"

    def route(self, path: str):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            regex_path = path.replace("<?>", "([^/]+)")
            self.routes[regex_path] = wrapper
            return wrapper
        return decorator


    def stop(self):
        self.running = False
        self.server_socket.close()
        print("Server stopped.")