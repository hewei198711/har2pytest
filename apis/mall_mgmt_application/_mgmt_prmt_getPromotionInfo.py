import os

from util.client import client

params = {
    "promotionId": 0,  # promotionId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_getPromotionInfo(params=params, headers=headers):
    """
    活动详情-活动信息
    /mgmt/prmt/getPromotionInfo

    参数说明:
    - promotionId: promotionId
    """

    url = "/mgmt/prmt/getPromotionInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
