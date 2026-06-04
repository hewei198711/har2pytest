import os

from util.client import client

data = {
    "cardNos": [],  # 会员卡号
    "ids": [],  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_deleteDisableUserById(data=data, headers=headers):
    """
    批量删除活动不可参与顾客（卡号删缓存，id删库）
    /mgmt/prmt/deleteDisableUserById

    参数说明:
    - cardNos: 会员卡号
    - ids: id
    """

    url = "/mgmt/prmt/deleteDisableUserById"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
