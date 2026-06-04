import os

from util.client import client

data = {
    "ids": [],  # 提交合同的主键id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_submitContract(data=data, headers=headers):
    """
    批量提交合同
    /mgmt/store/submitContract

    参数说明:
    - ids: 提交合同的主键id
    """

    url = "/mgmt/store/submitContract"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
