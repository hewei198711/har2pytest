import os
from urllib.parse import urlencode

from util.client import client

data = {
    "data": "",  # data
    "key": "",  # key
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _appStore_orderSign_sendSignRecissionCodeNew(data=data, headers=headers):
    """
    发送签约购解约验证码（加密）
    /appStore/orderSign/sendSignRecissionCodeNew

    参数说明:
    - data: data
    - key: key
    """

    url = "/appStore/orderSign/sendSignRecissionCodeNew"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
