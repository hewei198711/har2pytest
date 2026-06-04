import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_getSecondCouponExplain(headers=headers):
    """
    获取秒返券说明
    /mgmt/fin/wallet/getSecondCouponExplain
    """

    url = "/mgmt/fin/wallet/getSecondCouponExplain"
    with client.get(url=url, headers=headers) as r:
        return r
