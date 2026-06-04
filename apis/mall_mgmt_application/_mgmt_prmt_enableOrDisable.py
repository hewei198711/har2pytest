import os

from util.client import client

data = {
    "ids": [],  # TODO: 添加参数说明
    "memberState": 0,  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_enableOrDisable(data=data, headers=headers):
    """
    活动顾客的启用与禁用
    /mgmt/prmt/enableOrDisable
    """

    url = "/mgmt/prmt/enableOrDisable"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
