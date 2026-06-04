import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_fin_wallet_credit_importAdjustBatchDetail(headers=headers):
    """
    信用额调整批次详情-导入
    /mgmt/fin/wallet/credit/importAdjustBatchDetail
    """

    url = "/mgmt/fin/wallet/credit/importAdjustBatchDetail"
    with client.post(url=url, headers=headers) as r:
        return r
