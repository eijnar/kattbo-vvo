import requests
from urllib import parse

message = 'Hej, vi planerar en älgjakt '
number = '+702598032'

url = 'http://172.20.10.9:8080/send'


headers = {
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = {
    'message': message,
    'phoneno': number
}

send = requests.post(url, data, headers)

for i in send:
    print(i)
