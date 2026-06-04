import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_giftPromotion_delGiftCardPict(data=data, headers=headers):
    """
    送礼贺卡图片删除
    /mgmt/cms/giftPromotion/delGiftCardPict

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/giftPromotion/delGiftCardPict"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
