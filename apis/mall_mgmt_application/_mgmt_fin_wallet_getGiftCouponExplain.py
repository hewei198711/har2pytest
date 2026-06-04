import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_getGiftCouponExplain(headers=headers):
    """
    获取电子礼券说明
    /mgmt/fin/wallet/getGiftCouponExplain
    """

    url = "/mgmt/fin/wallet/getGiftCouponExplain"
    with client.get(url=url, headers=headers) as r:
        return r
