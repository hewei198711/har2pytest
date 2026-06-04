import os

from util.client import client

data = {
    "id": 0,  # 批次ID
    "increaseEndTime": "",  # 增加结束时间
    "increaseStartTime": "",  # 增加开始时间
    "reduceTime": "",  # 扣减时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_updateBatch(data=data, headers=headers):
    """
    云商信用额录入批次列表修改
    /mgmt/fin/wallet/credit/updateBatch

    参数说明:
    - id: 批次ID
    - increaseEndTime: 增加结束时间
    - increaseStartTime: 增加开始时间
    - reduceTime: 扣减时间
    """

    url = "/mgmt/fin/wallet/credit/updateBatch"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
