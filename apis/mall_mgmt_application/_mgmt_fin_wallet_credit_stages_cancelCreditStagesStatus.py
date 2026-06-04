import os

from util.client import client

data = {
    "creditStagesCode": "",  # 信用额分期管理编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_stages_cancelCreditStagesStatus(data=data, headers=headers):
    """
    终止信用额分期数据
    /mgmt/fin/wallet/credit/stages/cancelCreditStagesStatus

    参数说明:
    - creditStagesCode: 信用额分期管理编码
    """

    url = "/mgmt/fin/wallet/credit/stages/cancelCreditStagesStatus"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
