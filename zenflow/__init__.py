from typing import List, Callable
from .const import HTTP_METHODS, STATUS_CODES
from .request import Request
from .response import Response
import socket


class Route:
    def __init__(self, path: str, method: List[HTTP_METHODS], handler: Callable):
        self.path = path
        self.method = method
        self.handler = handler
    
    def check(self, request_path) -> tuple[bool, list]:
        arguments = []
        path_parts = [i for i in self.path.split('/') if i != ""]
        request_parts = [i for i in request_path.split('/') if i != ""]
        print("__eq__, parts: ", path_parts, request_parts)
        
        if len(path_parts) != len(request_parts):
            return (False, [])
        for i, j in zip(path_parts, request_parts):
            if i != j and i != "<?>":
                return (False, [])
            elif i == "<?>":
                arguments.append(j)
        return (True, arguments)
    
    def __contains__(self, __value: object) -> bool:
        return __value in self.method
    
    
    def __call__(self, request: 'Request', *args, **kwargs):
        print("__call__, args: ", args, kwargs)
        print("-> args:", len(args), "co_argcount", self.handler.__code__.co_argcount)
        if self.handler.__code__.co_argcount == 1:
            return self.handler(request)
        elif self.handler.__code__.co_argcount == len(args) + 1:
            return self.handler(request, *args)
        else:
            raise Exception("Too many arguments in handler function.")
        
    def __repr__(self) -> str:
        return f"<Route {self.method} {self.path} {self.handler}>"
   
        


class Server:
    def __init__(self, host='127.0.0.1', port=8000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.running = True
        self.routes: List[Route] = []

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
                    request = Request(conn.recv(1024).decode('utf-8'))
                    response = self.route_request(request)
                    conn.sendall(str(response).encode('utf-8'))
        except KeyboardInterrupt:
            print("Keyboard Interrupt received, stopping server.")
        finally:
            self.stop()


    def route_request(self, request: Request) -> Response:
        # Match the paroutes = {}  # Global dictionary to store routes and their handlers

        for route in self.routes:
            if request.method not in route:
                continue
            match, arguments = route.check(request.url)
            if not match:
                continue
            try:
                response = route(request, *arguments)
                if isinstance(response, Template):
                    path, status = response.render()
                    with open(path, 'r') as f:
                        return Response("200 OK", body=f.read())
                elif isinstance(response, Response):
                    return response
                elif isinstance(response, str):
                    return Response("200 OK", body=response)
                else:
                    return Response("200 OK", body=str(response))
            except Exception as e:
                print(e)
                return Response("500 Internal Server Error", body="500 Internal Server Error")
            
        return Response("404 Not Found", body="404 Not Found")

    def route(self, path: str, method: List[HTTP_METHODS] | None = None):
        if method is None:
            method = ['GET']
        
        def decorator(func):
            self.routes.append(Route(path, method, func))
            return func
        return decorator

    def stop(self):
        self.running = False
        self.server_socket.close()
        print("Server stopped.")




class Template:
    def __init__(self, path: str, status: STATUS_CODES = "200 OK"):
        self.path = path
        self.status = status

    def render(self, **kwargs):
        for key, value in kwargs.items():
            self.path = self.path.replace(f"{{{{{key}}}}}", value)
        return self.path, self.status

