import os

from util.client import client

data = {
    "idList": [],  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_loginGift_disabledMembers(data=data, headers=headers):
    """
    批量禁用顾客
    /mgmt/prmt/loginGift/disabledMembers
    """

    url = "/mgmt/prmt/loginGift/disabledMembers"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
