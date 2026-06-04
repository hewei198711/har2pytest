import os

from util.client import client

params = {
    "withdrawId": 0,  # withdrawId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_second_coupon_queryWithdrawdtlList(params=params, headers=headers):
    """
    秒返券提现详情查询
    /mgmt/fin/voucher/second/coupon/queryWithdrawdtlList

    参数说明:
    - withdrawId: withdrawId
    """

    url = "/mgmt/fin/voucher/second/coupon/queryWithdrawdtlList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
