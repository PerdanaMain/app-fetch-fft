from database import getConnection
from requests import get, post
from config import Config
from api.auth import login


def get_all_tags():
    try:
        token = login()
        
        res = get(Config.API_SERVER+"/pfi/api/v1/tags", headers={
                "Authorization": "Bearer "+ token
            })
        tags = res.json()["data"]
        
        return tags
    except Exception as e:
      print('An exception occurred: ', e)


def create_tag(data):
    try:
      token = login()
      
      post(Config.API_SERVER+"/pfi/api/v1/tag-values", headers={
        "Authorization": "Bearer "+ token
        }, json={
        "data": data
      })
    except Exception as e:
      print('An exception occurred: ', e)
