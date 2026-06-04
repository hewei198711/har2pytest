import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "from": 0,  # TODO: 添加参数说明
    "memberType": 0,  # 会员类别：1->普通顾客；2->优惠顾客；3->云商；4->微店（云+）；5->店员；6->子账号
    "mobile": "",  # 手机号码
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "shopCode": "",  # 服务中心编码
    "surveyStatus": 0,  # 礼券调查  1：礼券200 2：礼券800 3：不要礼券
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_gift_coupon_queryGiftCouponSurvey(data=data, headers=headers):
    """
    电子礼券调查明细查询接口（商城后台）
    /mgmt/fin/voucher/gift/coupon/queryGiftCouponSurvey

    参数说明:
    - cardNo: 会员卡号
    - memberType: 会员类别：1->普通顾客；2->优惠顾客；3->云商；4->微店（云+）；5->店员；6->子账号
    - mobile: 手机号码
    - pageNum: 页数
    - pageSize: 每页显示数
    - shopCode: 服务中心编码
    - surveyStatus: 礼券调查  1：礼券200 2：礼券800 3：不要礼券
    """

    url = "/mgmt/fin/voucher/gift/coupon/queryGiftCouponSurvey"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
