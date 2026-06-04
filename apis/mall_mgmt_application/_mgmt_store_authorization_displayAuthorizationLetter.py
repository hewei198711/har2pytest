import os
from urllib.parse import urlencode

from util.client import client

data = {
    "id": 0,  # id
    "isShow": 0,  # 是否显示于门店系统，0：否，1：是
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_authorization_displayAuthorizationLetter(data=data, headers=headers):
    """
    隐藏/显示授权书
    /mgmt/store/authorization/displayAuthorizationLetter

    参数说明:
    - id: id
    - isShow: 是否显示于门店系统，0：否，1：是
    """

    url = "/mgmt/store/authorization/displayAuthorizationLetter"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
