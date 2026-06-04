import os

from util.client import client

params = {
    "promotionCode": "",  # promotionCode
    "promotionName": "",  # promotionName
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_getPromotionByCodeOrName(params=params, headers=headers):
    """
    根据活动编码或名称搜索活动
    /mgmt/prmt/coupon/getPromotionByCodeOrName

    参数说明:
    - promotionCode: promotionCode
    - promotionName: promotionName
    """

    url = "/mgmt/prmt/coupon/getPromotionByCodeOrName"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
