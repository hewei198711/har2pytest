import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_second_coupon_queryDetail(headers=headers):
    """
    秒返券详情
    /mgmt/fin/voucher/second/coupon/queryDetail
    """

    url = "/mgmt/fin/voucher/second/coupon/queryDetail"
    with client.get(url=url, headers=headers) as r:
        return r
