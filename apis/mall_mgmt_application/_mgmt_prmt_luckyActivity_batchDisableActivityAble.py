import os

from util.client import client

data = {
    "idList": [],  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_batchDisableActivityAble(data=data, headers=headers):
    """
    批量禁用活动顾客
    /mgmt/prmt/luckyActivity/batchDisableActivityAble
    """

    url = "/mgmt/prmt/luckyActivity/batchDisableActivityAble"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
