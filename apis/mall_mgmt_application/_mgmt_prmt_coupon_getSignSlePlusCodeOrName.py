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


def _mgmt_prmt_coupon_getSignSlePlusCodeOrName(params=params, headers=headers):
    """
    根据活动编码或名称搜索签约购3.0活动
    /mgmt/prmt/coupon/getSignSlePlusCodeOrName

    参数说明:
    - promotionCode: promotionCode
    - promotionName: promotionName
    """

    url = "/mgmt/prmt/coupon/getSignSlePlusCodeOrName"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
