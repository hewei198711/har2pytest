import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_fin_wallet_credit_importApply(headers=headers):
    """
    顾客信用额列表-批量导入
    /mgmt/fin/wallet/credit/importApply
    """

    url = "/mgmt/fin/wallet/credit/importApply"
    with client.post(url=url, headers=headers) as r:
        return r
