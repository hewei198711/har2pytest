import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_fin_wallet_credit_getBatchList(headers=headers):
    """
    云商信用额录入批次列表
    /mgmt/fin/wallet/credit/getBatchList
    """

    url = "/mgmt/fin/wallet/credit/getBatchList"
    with client.post(url=url, headers=headers) as r:
        return r
