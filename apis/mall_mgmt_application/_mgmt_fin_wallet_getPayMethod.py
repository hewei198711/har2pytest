import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_fin_wallet_getPayMethod(headers=headers):
    """
    获取支付方式
    /mgmt/fin/wallet/getPayMethod
    """

    url = "/mgmt/fin/wallet/getPayMethod"
    with client.post(url=url, headers=headers) as r:
        return r
