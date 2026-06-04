import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_giftPromotion_delGiftCardText(data=data, headers=headers):
    """
    送礼贺卡文案删除
    /mgmt/cms/giftPromotion/delGiftCardText

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/giftPromotion/delGiftCardText"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
