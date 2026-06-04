import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_gift_coupon_queryWithdrawconf(headers=headers):
    """
    电子礼券提现配置查询
    /mgmt/fin/voucher/gift/coupon/queryWithdrawconf
    """

    url = "/mgmt/fin/voucher/gift/coupon/queryWithdrawconf"
    with client.get(url=url, headers=headers) as r:
        return r
