import zenflow


server = zenflow.Server()


@server.route("/", ["GET"])
def index(request: zenflow.Request):
    return "HTTP/1.1 200 OK\n\n<h1>Hello World</h1>"

@server.route("/test", ["GET"])
def test(request: zenflow.Request):
    return "HTTP/1.1 200 OK\n\n<h1>Test</h1>"

@server.route("/api/<?>", ["GET"])
def api(request: zenflow.Request, user_id):
    return f"HTTP/1.1 200 OK\n\n<h1>Hello, {user_id}</h1>"

@server.route("/users/<?>/<?>", ["GET"])
def users(request: zenflow.Request, username, message):
    return f"HTTP/1.1 200 OK\n\n<h1>Profile of {username}, message:{message}</h1>"

server.start()
