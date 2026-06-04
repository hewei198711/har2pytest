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


def _mgmt_prmt_coupon_getComplexCodeOrName(params=params, headers=headers):
    """
    根据活动编码或名称搜索签约购4.0活动
    /mgmt/prmt/coupon/getComplexCodeOrName

    参数说明:
    - promotionCode: promotionCode
    - promotionName: promotionName
    """

    url = "/mgmt/prmt/coupon/getComplexCodeOrName"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
