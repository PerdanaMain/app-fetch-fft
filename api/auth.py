from requests import get, post
from config import Config

def login():
    try:
        res = post(Config.API_SERVER+"/auth/sign-in", json={
            "username": Config.API_USERNAME,
            "password": Config.API_PASSWORD
        })
        auth = res.json()["data"]
        
        if res.status_code == 200:
            token = refresh_token(auth["refresh_token"])
            return token
    except Exception as e:
        print('An exception occurred: ', e)
        return None
      
def refresh_token(refresh_token):
    try:
        res = get(Config.API_SERVER+"/auth/refresh-token", headers={
                "Authorization": "Bearer "+ refresh_token
            })
        
        auth = res.json()["data"]
        
        if res.status_code == 200:
            return auth["access_token"]
    except Exception as e:
        print('An exception occurred: ', e)
        return None