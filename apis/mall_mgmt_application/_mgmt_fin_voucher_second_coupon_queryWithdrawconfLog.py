import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_second_coupon_queryWithdrawconfLog(headers=headers):
    """
    秒返券提现配置修改记录查询
    /mgmt/fin/voucher/second/coupon/queryWithdrawconfLog
    """

    url = "/mgmt/fin/voucher/second/coupon/queryWithdrawconfLog"
    with client.get(url=url, headers=headers) as r:
        return r
