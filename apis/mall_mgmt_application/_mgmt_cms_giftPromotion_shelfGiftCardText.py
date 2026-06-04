import os

from util.client import client

data = {
    "id": 0,  # id
    "shelfOperate": 0,  # 上下架操作: 1:上架(发布); 2:下架;
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_giftPromotion_shelfGiftCardText(data=data, headers=headers):
    """
    送礼贺卡文案上下架
    /mgmt/cms/giftPromotion/shelfGiftCardText

    参数说明:
    - id: id
    - shelfOperate: 上下架操作: 1:上架(发布); 2:下架;
    """

    url = "/mgmt/cms/giftPromotion/shelfGiftCardText"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
