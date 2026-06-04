import os

from util.client import client

data = {
    "createTimeEnd": "",  # 创建时间范围结束
    "createTimeStart": "",  # 创建时间范围开始
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "pictName": "",  # 图片名称
    "pictNo": "",  # 图片编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_giftPromotion_queryGiftCardPictPage(data=data, headers=headers):
    """
    送礼贺卡图片分页列表查询
    /mgmt/cms/giftPromotion/queryGiftCardPictPage

    参数说明:
    - createTimeEnd: 创建时间范围结束
    - createTimeStart: 创建时间范围开始
    - pageNum: 页码
    - pageSize: 每页页数
    - pictName: 图片名称
    - pictNo: 图片编号
    """

    url = "/mgmt/cms/giftPromotion/queryGiftCardPictPage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
