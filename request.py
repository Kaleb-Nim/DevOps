import requests
url = 'http://localhost:5000/api'
r = requests.post(url,json = {'testing':1.8,'feature2':2.8})

# print(r.json())
