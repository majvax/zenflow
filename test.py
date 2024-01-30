import zenflow
from zenflow.response import Response
import json
import base64

server = zenflow.Server(port=8080)


@server.route("/", ["GET"])
def index(request: zenflow.Request):
    return "HTTP/1.1 200 OK\n\n<h1>Hello World</h1>"

@server.route("/test", ["GET"])
def test(request: zenflow.Request):
    return "HTTP/1.1 200 OK\n\n<h1>Test</h1>"

@server.route("/api/<?>", ["GET"])
def api(request: zenflow.Request, user_id):
    return Response("200 OK", body=f"<h1>Hello, {user_id}</h1><br><h2>{request.json.get("name") if request.json else ""}</h2>")

@server.route("/users/<?>/<?>", ["GET"])
def users(request: zenflow.Request, username, message):
    return f"HTTP/1.1 200 OK\n\n<h1>Profile of {username}, message:{message}</h1>"


@server.route("/api", ["POST", "PUT"])
def api_(request: zenflow.Request):

    if request.method == "PUT":
        return Response("200 OK", body=f"<h1>PUT</h1>")
    elif request.method == "POST":
        name = request.json.get("name")
        return Response("200 OK", body=f"<h1>POST | {name}</h1>")

    return Response("401 Unauthorized", body="401 Unauthorized")
    

@server.route("/api", ["DELETE"])
def api__(request: zenflow.Request):

    name = request.json.get("name")
    if name is not None:
        return Response("200 OK", body=json.dumps({"status": "success"}))

    return Response("200 OK", body=json.dumps({"status": "failed"}))

@server.route("/login", ["POST"])
def login_post(request: zenflow.Request):
    name = request.json.get("name")
    password = request.json.get("password")

    if name == "admin" and password == "admin":
        token = base64.b64encode(f"{name}:{password}".encode('utf-8')).decode('utf-8')
    
        return Response("200 OK", body=json.dumps({"status": "success",}), headers={"Set-Cookie": f"token={token}; HttpOnly; Path=/"})

    return Response("200 OK", body=json.dumps({"status": "failed"}))


@server.route("/login", ["GET"])
def login_get(request: zenflow.Request):
    token = request.cookies.get("token")

    
    if token is not None:
        name, password = base64.b64decode(token).decode('utf-8').split(":")
        if name == "admin" and password == "admin":
            return Response("200 OK", body=json.dumps({"status": "success"}))

    return Response("200 OK", body=json.dumps({"status": "failed"}))


server.start()
