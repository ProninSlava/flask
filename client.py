import requests

data = requests.get('http://127.0.0.1:5000/hello/', json={'a':'b'}, params={'key':'value'})
print(data.status_code)
print(data.text)