import os

from util.client import client

data = {
    "giftCardText": "",  # 贺卡文案
    "id": 0,  # id(编辑时)
    "shelfStatus": 0,  # 上下架状态: 1:上架(发布); 2:下架;
    "textNo": "",  # 文案编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_giftPromotion_editGiftCardText(data=data, headers=headers):
    """
    送礼贺卡文案编辑
    /mgmt/cms/giftPromotion/editGiftCardText

    参数说明:
    - giftCardText: 贺卡文案
    - id: id(编辑时)
    - shelfStatus: 上下架状态: 1:上架(发布); 2:下架;
    - textNo: 文案编号
    """

    url = "/mgmt/cms/giftPromotion/editGiftCardText"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
