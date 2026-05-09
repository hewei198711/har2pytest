import os
from urllib.parse import urlencode

from util.client import client

data = {
    "signNo": "",  # signNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _appStore_orderSign_signRecission(data=data, headers=headers):
    """
    签约购解约
    /appStore/orderSign/signRecission

    参数说明:
    - signNo: signNo
    """

    url = "/appStore/orderSign/signRecission"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
