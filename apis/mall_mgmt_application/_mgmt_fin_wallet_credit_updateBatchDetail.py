import os

from util.client import client

data = {
    "batchId": 0,  # 批次ID
    "batchdtlId": 0,  # 批次详情ID
    "cardNo": "",  # 会员卡号
    "increaseAmount": 0.0,  # 增加信用额
    "walletId": 0,  # 钱包ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_updateBatchDetail(data=data, headers=headers):
    """
    云商信用额录入批次详情列表修改
    /mgmt/fin/wallet/credit/updateBatchDetail

    参数说明:
    - batchId: 批次ID
    - batchdtlId: 批次详情ID
    - cardNo: 会员卡号
    - increaseAmount: 增加信用额
    - walletId: 钱包ID
    """

    url = "/mgmt/fin/wallet/credit/updateBatchDetail"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
