import base64
import requests


def get_token(username, password):
    try:
        your_string = f"{username}:{password}"
        b = base64.b64encode(your_string.encode('utf-8'))
        url = "https://qtoss-connect.azurewebsites.net/token"
        base64_str = b.decode('utf-8')
        authorization = 'Basic ' + base64_str
        response = requests.post(url=url, headers={'Content-Type': 'application/json',
                                                   'Authorization': authorization})
        data = response.json()
        access_token = data['access_token']
        if response.status_code == 200:
            return base64_str, access_token
        else:
            return None
    except Exception as e:
        print(e)
        return None


aa = get_token("song", "306012")
