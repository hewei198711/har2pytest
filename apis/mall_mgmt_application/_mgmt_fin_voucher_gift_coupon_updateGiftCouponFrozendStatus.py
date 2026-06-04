import os

from util.client import client

data = {
    "grantdtlIdList": [],  # 电子礼券发放明细编号
    "operationContent": 0,  # 操作内容 1:冻结 2:解冻
    "remark": "",  # 备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_gift_coupon_updateGiftCouponFrozendStatus(data=data, headers=headers):
    """
    电子礼券冻结解冻接口（商城后台）
    /mgmt/fin/voucher/gift/coupon/updateGiftCouponFrozendStatus

    参数说明:
    - grantdtlIdList: 电子礼券发放明细编号
    - operationContent: 操作内容 1:冻结 2:解冻
    - remark: 备注
    """

    url = "/mgmt/fin/voucher/gift/coupon/updateGiftCouponFrozendStatus"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
