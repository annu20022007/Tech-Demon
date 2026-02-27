import requests
import time

base = "http://localhost:8001/api"
root = "http://localhost:8001"

print("root health", requests.get(root+"/health").status_code)

# register and login to obtain token
email = f"user_test_{int(time.time())}@example.com"
password = "Pass1234"
print("registering", email)
reg = requests.post(base+"/auth/register", json={"name":"Test","email":email,"password":password})
print("register status", reg.status_code, reg.text)
if reg.status_code==200:
    login = requests.post(base+"/auth/login", json={"email":email,"password":password})
    print("login status", login.status_code, login.text)
    if login.status_code==200:
        token = login.json().get("access_token")
    else:
        token = None
else:
    token = None

headers = {"Authorization": f"Bearer {token}"} if token else {}
# test additional endpoints
endpoints = [
    ("get","/dashboard/stats"),
    ("get","/dashboard/performance"),
    ("get","/dashboard/sentiment"),
    ("get","/dashboard/insight"),
    ("get","/learning/modules"),
    ("get","/prediction/analyze"),
    ("post","/prediction/submit",{"dummy":1}),
    ("get","/news/feed"),
    ("post","/news/sentiment",{"article":"test"}),
    ("get","/portfolio/history"),
    ("get","/portfolio/insight"),
    ("post","/advisor/recommendations",{"portfolioValue":10000}),
    ("post","/advisor/chat",{"message":"hello"}),
    ("post","/advisor/portfolio-analysis",{"holdings":[]})
]

for req in endpoints:
    method = req[0]
    path = req[1]
    data = req[2] if len(req) > 2 else {}
    try:
        if method == "get":
            r = requests.get(base+path, headers=headers, timeout=5)
        else:
            r = requests.post(base+path, headers=headers, json=data, timeout=5)
        print(path, r.status_code)
    except Exception as e:
        print(path, "ERR", e)
