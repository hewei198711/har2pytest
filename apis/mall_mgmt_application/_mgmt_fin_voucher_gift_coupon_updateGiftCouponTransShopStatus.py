import os

from util.client import client

data = {
    "grantdtlIdList": [],  # 电子礼券发放明细编号
    "ifNotUsed": False,  # TODO: 添加参数说明
    "shopCode": "",  # TODO: 添加参数说明
    "transInshopCode": "",  # 转入服务中心编码
    "transInshopName": "",  # 转入服务中心名称
    "transShopTime": "",  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_gift_coupon_updateGiftCouponTransShopStatus(data=data, headers=headers):
    """
    电子礼券转店接口（商城后台）
    /mgmt/fin/voucher/gift/coupon/updateGiftCouponTransShopStatus

    参数说明:
    - grantdtlIdList: 电子礼券发放明细编号
    - transInshopCode: 转入服务中心编码
    - transInshopName: 转入服务中心名称
    """

    url = "/mgmt/fin/voucher/gift/coupon/updateGiftCouponTransShopStatus"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
