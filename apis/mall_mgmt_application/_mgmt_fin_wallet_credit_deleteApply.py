import os

from util.client import client

data = {
    "walletCreditApplyIdList": [],  # 顾客信用额申请id集合
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_deleteApply(data=data, headers=headers):
    """
    顾客信用额列表-删除
    /mgmt/fin/wallet/credit/deleteApply

    参数说明:
    - walletCreditApplyIdList: 顾客信用额申请id集合
    """

    url = "/mgmt/fin/wallet/credit/deleteApply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
