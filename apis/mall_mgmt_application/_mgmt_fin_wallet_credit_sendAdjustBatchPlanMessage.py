import os

from util.client import client

params = {
    "creditAdjustBatchId": 0,  # 调整批次id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_sendAdjustBatchPlanMessage(params=params, headers=headers):
    """
    信用额调整批次审核通过发送站内信
    /mgmt/fin/wallet/credit/sendAdjustBatchPlanMessage

    参数说明:
    - creditAdjustBatchId: 调整批次id
    """

    url = "/mgmt/fin/wallet/credit/sendAdjustBatchPlanMessage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
