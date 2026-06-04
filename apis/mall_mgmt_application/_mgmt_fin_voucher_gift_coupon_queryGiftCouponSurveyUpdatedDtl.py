import os
from urllib.parse import urlencode

from util.client import client

data = {
    "surveydtlId": 0,  # 电子礼券调查id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_fin_voucher_gift_coupon_queryGiftCouponSurveyUpdatedDtl(data=data, headers=headers):
    """
    电子礼券调查明细变更记录查询接口（商城后台）
    /mgmt/fin/voucher/gift/coupon/queryGiftCouponSurveyUpdatedDtl

    参数说明:
    - surveydtlId: 电子礼券调查id
    """

    url = "/mgmt/fin/voucher/gift/coupon/queryGiftCouponSurveyUpdatedDtl"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
