# curl --location 'https://qtoss-connect-dev.azurewebsites.net/token' \
# --header 'Content-Type: application/json' \
# --header 'Authorization: Basic YWRtaW5AZ21haWwuY29tOjEyMzQ1Ng==' \
# --data-raw '{
#   "firstName": "Haiping",
#   "lastName": "Chen",
#   "email": "admin@gmail.com",
#   "password": "123456"
# }'

'''
import base64
# Your string to encode
your_string = "haiping008@gmail.com:123456"

# Encode the string to Base64
b = base64.b64encode(your_string.encode('utf-8'))

# Convert bytes to a string
base64_str = b.decode('utf-8')
'''

import json
import base64
import requests


def login():
    # Your string to encode
    your_string = "song:306012"

    b = base64.b64encode(your_string.encode('utf-8'))
    url = "https://qtoss-connect.azurewebsites.net/token"
    base64_str = b.decode('utf-8')
    dd = 'Basic ' + base64_str
    res = requests.post(url=url, headers={'Content-Type': 'application/json',
                                          'Authorization': dd})
    res = json.loads(res.text)
    return res['access_token']


token = login()
print(token)

'''
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiI1ZDVkMGU4MS1lNGE2LTQ3Y2QtYjAyNy03ZWU2ZTE2ZjRmYmMiLCJ1bmlxdWVfbmFtZSI6InNvbmciLCJlbWFpbCI6IjIxODEyNTE4NDNAcXEuY29tIiwiZ2l2ZW5fbmFtZSI6InNvbmciLCJmYW1pbHlfbmFtZSI6IiIsInNvdXJjZSI6ImludGVybmFsIiwiZXh0ZXJuYWxfaWQiOiIiLCJqdGkiOiIwOTY2NjE0Yy0wYjNhLTQ5ZWYtODQ1NS01MmJjZTc2OWZjZWEiLCJwaG9uZSI6IiIsIm5iZiI6MTcyMzcxNjI3NSwiZXhwIjoxNzIzNzIzNDc1LCJpYXQiOjE3MjM3MTYyNzUsImlzcyI6InF0b3NzIiwiYXVkIjoicXRvc3MifQ.TUJVU7x5Yx_QI_RAuizl5HJv4iDuld3zfau6C0st1-0

'''
