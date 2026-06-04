import os

from util.client import client

data = {
    "id": 0,  # id(编辑时)
    "pictName": "",  # 图片名称
    "pictNo": "",  # 图片编号
    "pictUrl": "",  # 贺卡图片
    "shelfStatus": 0,  # 上下架状态: 1:上架(发布); 2:下架;
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_giftPromotion_saveGiftCardPict(data=data, headers=headers):
    """
    送礼贺卡图片新增
    /mgmt/cms/giftPromotion/saveGiftCardPict

    参数说明:
    - id: id(编辑时)
    - pictName: 图片名称
    - pictNo: 图片编号
    - pictUrl: 贺卡图片
    - shelfStatus: 上下架状态: 1:上架(发布); 2:下架;
    """

    url = "/mgmt/cms/giftPromotion/saveGiftCardPict"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
