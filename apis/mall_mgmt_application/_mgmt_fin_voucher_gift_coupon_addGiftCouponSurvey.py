import os

from util.client import client

data = {
    "memberId": 0,  # 用户id
    "surveyStatus": 0,  # 礼券调查状态 1：礼券200 2：礼券800 3：不要礼券
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_gift_coupon_addGiftCouponSurvey(data=data, headers=headers):
    """
    电子礼券调查添加接口（商城后台）
    /mgmt/fin/voucher/gift/coupon/addGiftCouponSurvey

    参数说明:
    - memberId: 用户id
    - surveyStatus: 礼券调查状态 1：礼券200 2：礼券800 3：不要礼券
    """

    url = "/mgmt/fin/voucher/gift/coupon/addGiftCouponSurvey"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
