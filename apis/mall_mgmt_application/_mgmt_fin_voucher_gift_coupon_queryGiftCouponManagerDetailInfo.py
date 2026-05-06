from urllib.parse import urlencode

from util.client import client

data = {
    "grantdtlId": "2043868590615973888",  # 电子礼券发放id号
}

headers = {"channel": "pc", "client": "op", "authorization": "请输入认证令牌"}


def _mgmt_fin_voucher_gift_coupon_queryGiftCouponManagerDetailInfo(data=data, headers=headers):
    """
    电子礼券管理界面查询详情接口（商城后台）
    /mgmt/fin/voucher/gift/coupon/queryGiftCouponManagerDetailInfo

    参数说明:
    - grantdtlId: 电子礼券发放id号
    """

    url = "/mgmt/fin/voucher/gift/coupon/queryGiftCouponManagerDetailInfo"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
