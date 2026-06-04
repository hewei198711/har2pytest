import os
from urllib.parse import urlencode

from util.client import client

data = {
    "isShow": 0,  # 是否显示于门店系统，0：否，1：是
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_authorization_batchDisplayAuthorizationLetter(data=data, headers=headers):
    """
    批量隐藏/显示授权书
    /mgmt/store/authorization/batchDisplayAuthorizationLetter

    参数说明:
    - isShow: 是否显示于门店系统，0：否，1：是
    """

    url = "/mgmt/store/authorization/batchDisplayAuthorizationLetter"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
