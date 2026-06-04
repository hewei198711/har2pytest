import os

from util.client import client

params = {
    "promotionCode": "",  # promotionCode
    "promotionId": 0,  # promotionId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_selectPromotionCode(params=params, headers=headers):
    """
    查询活动编码是否已经存在
    /mgmt/prmt/selectPromotionCode

    参数说明:
    - promotionCode: promotionCode
    - promotionId: promotionId
    """

    url = "/mgmt/prmt/selectPromotionCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
