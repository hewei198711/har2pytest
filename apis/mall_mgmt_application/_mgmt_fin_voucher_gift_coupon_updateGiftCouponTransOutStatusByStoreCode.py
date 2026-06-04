import os

from util.client import client

params = {
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_gift_coupon_updateGiftCouponTransOutStatusByStoreCode(params=params, headers=headers):
    """
    业务大厅结业申请审核通过电子礼券转出接口（商城后台）
    /mgmt/fin/voucher/gift/coupon/updateGiftCouponTransOutStatusByStoreCode

    参数说明:
    - storeCode: 服务中心编号
    """

    url = "/mgmt/fin/voucher/gift/coupon/updateGiftCouponTransOutStatusByStoreCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
