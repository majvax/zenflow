import socket
import re
from functools import wraps
from typing import Callable, Dict, Any, List


class Server:
    def __init__(self, host='127.0.0.1', port=8000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.running = True
        self.routes: Dict = {}

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
                    print("----------------")
                    print(f"{request}\n{path}\n{response}")
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

    def route(self, path: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(func)
            def wrapper(*args: List, **kwargs: Dict) -> Any:
                return func(*args, **kwargs)
            regex_path = path.replace("<?>", "([^/]+)")
            self.routes[regex_path] = wrapper
            return wrapper
        return decorator


    def stop(self):
        self.running = False
        self.server_socket.close()
        print("Server stopped.")

# Example usage of the route decorator



if __name__ == "__main__":
    server = Server()
    
    @server.route("/user/<?>")
    def user(user_id):
        return f"HTTP/1.1 200 OK\n\nUser Page for {user_id}"
    print(server.routes)
    server.start()
