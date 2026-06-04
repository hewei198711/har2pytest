import os

from util.client import client

params = {
    "withdrawId": 0,  # withdrawId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_gift_coupon_queryWithdrawdtlList(params=params, headers=headers):
    """
    电子礼券提现详情查询
    /mgmt/fin/voucher/gift/coupon/queryWithdrawdtlList

    参数说明:
    - withdrawId: withdrawId
    """

    url = "/mgmt/fin/voucher/gift/coupon/queryWithdrawdtlList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
