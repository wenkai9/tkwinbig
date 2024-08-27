import base64
import requests


def get_token():
    try:
        your_string = "2181251843@qq.com:306012"
        b = base64.b64encode(your_string.encode('utf-8'))
        url = "https://qtoss-connect.azurewebsites.net/token"
        base64_str = b.decode('utf-8')
        authorization = 'Basic ' + base64_str
        response = requests.post(url=url, headers={'Content-Type': 'application/json',
                                                   'Authorization': authorization})
        data = response.json()
        access_token = data['access_token']
        if response.status_code == 200:
            return access_token
        else:
            return None
    except Exception as e:
        print(e)
        return None
