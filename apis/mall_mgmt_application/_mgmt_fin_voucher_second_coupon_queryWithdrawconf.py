import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_second_coupon_queryWithdrawconf(headers=headers):
    """
    秒返券提现配置查询
    /mgmt/fin/voucher/second/coupon/queryWithdrawconf
    """

    url = "/mgmt/fin/voucher/second/coupon/queryWithdrawconf"
    with client.get(url=url, headers=headers) as r:
        return r
