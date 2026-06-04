import os

from util.client import client

data = {
    "secondCouponIdList": [],  # 秒返券id集合
    "withdrawReason": "",  # 提现原因
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_mgmtSecondCouponWithdraw(data=data, headers=headers):
    """
    秒返券后台提现
    /mgmt/fin/voucher/mgmtSecondCouponWithdraw

    参数说明:
    - secondCouponIdList: 秒返券id集合
    - withdrawReason: 提现原因
    """

    url = "/mgmt/fin/voucher/mgmtSecondCouponWithdraw"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
