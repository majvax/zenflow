import requests
import json



# r = requests.get("http://localhost:8080/", headers={"User-Agent": "Zenflow"})
# print(r.headers)

r = requests.post("http://localhost:8080/api", json={"name": "application/json"})
print(r.request.body)
print(r.headers, r.text)
