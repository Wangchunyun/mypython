#-*-coding:utf-8-*-
# import sys
# sys.path.append('../common/')
import requests
import json
# import baseurl
# import headers
class Login():

    def login1(self):
        header = {
            'content-type': 'application/json'
        }
        url = 'https://xapi.xunai-tech.com/xunai-v2/api/jwt/v2/token'
        data = {
            'username': '18290107861',
            'password': '123456',
            'type': '2'
        }
        res = requests.post(url=url,data=json.dumps(data),headers=header)
        token = json.loads(res.text)['data']['token']
        print(token)
        return token


Login().login1()
# if __name__ == "__main__":
#     a = Login()
#     a.login1()