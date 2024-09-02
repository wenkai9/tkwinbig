import base64
import requests


def get_token(username, password):
    try:
        your_string = f"{username}:{password}"
        b = base64.b64encode(your_string.encode('utf-8'))
        url = "https://qtoss-connect.azurewebsites.net/token"
        base64_str = b.decode('utf-8')
        authorization = 'Basic ' + base64_str
        print("authorization", authorization)
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


def get_rpa_key(username, password):
    try:
        return base64.b64encode(f"{username}:{password}".encode('utf-8')).decode('utf-8')
    except Exception as e:
        print(f"Error: {e}")
        return None
