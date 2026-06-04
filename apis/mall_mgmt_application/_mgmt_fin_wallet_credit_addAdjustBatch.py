import os

from util.client import client

data = {
    "adjustBatchNo": "",  # 批次号
    "creditAdjBatchId": 0,  # 调整批次id，新增不传，修改必传
    "increaseEndTime": "",  # 增加结束时间
    "increaseStartTime": "",  # 增加开始时间
    "reduceTime": "",  # 扣减时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_addAdjustBatch(data=data, headers=headers):
    """
    信用额调整批次-新增
    /mgmt/fin/wallet/credit/addAdjustBatch

    参数说明:
    - adjustBatchNo: 批次号
    - creditAdjBatchId: 调整批次id，新增不传，修改必传
    - increaseEndTime: 增加结束时间
    - increaseStartTime: 增加开始时间
    - reduceTime: 扣减时间
    """

    url = "/mgmt/fin/wallet/credit/addAdjustBatch"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
