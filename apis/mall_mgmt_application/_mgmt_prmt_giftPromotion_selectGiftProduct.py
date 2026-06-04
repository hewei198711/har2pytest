import os

from util.client import client

params = {
    "serialNo": "",  # serialNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_giftPromotion_selectGiftProduct(params=params, headers=headers):
    """
    查询赠品活动中商品
    /mgmt/prmt/giftPromotion/selectGiftProduct

    参数说明:
    - serialNo: serialNo
    """

    url = "/mgmt/prmt/giftPromotion/selectGiftProduct"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
