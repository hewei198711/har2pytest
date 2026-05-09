import os
from urllib.parse import urlencode

from util.client import client

data = {
    "phoneNum": "",  # phoneNum
    "smsCode": "",  # smsCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _appStore_orderSign_validSignRecissionCode(data=data, headers=headers):
    """
    验证签约购解约验证码
    /appStore/orderSign/validSignRecissionCode

    参数说明:
    - phoneNum: phoneNum
    - smsCode: smsCode
    """

    url = "/appStore/orderSign/validSignRecissionCode"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
