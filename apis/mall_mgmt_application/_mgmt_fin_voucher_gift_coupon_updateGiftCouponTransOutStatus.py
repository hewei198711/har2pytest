import os

from util.client import client

data = {
    "grantdtlIdList": [],  # 电子礼券发放明细编号
    "transReason": "",  # 转出原因
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_gift_coupon_updateGiftCouponTransOutStatus(data=data, headers=headers):
    """
    电子礼券转出接口（商城后台）
    /mgmt/fin/voucher/gift/coupon/updateGiftCouponTransOutStatus

    参数说明:
    - grantdtlIdList: 电子礼券发放明细编号
    - transReason: 转出原因
    """

    url = "/mgmt/fin/voucher/gift/coupon/updateGiftCouponTransOutStatus"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
