import os

from util.client import client

data = {
    "batchdtlIdList": [],  # 调整批次详情ID集合
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_deleteAdjustBatchDetail(data=data, headers=headers):
    """
    信用额调整批次详情-删除
    /mgmt/fin/wallet/credit/deleteAdjustBatchDetail

    参数说明:
    - batchdtlIdList: 调整批次详情ID集合
    """

    url = "/mgmt/fin/wallet/credit/deleteAdjustBatchDetail"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
