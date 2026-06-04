import os

from util.client import client

data = {
    "createTimeEnd": "",  # 创建时间范围结束
    "createTimeStart": "",  # 创建时间范围开始
    "giftCardText": "",  # 文案内容
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "textNo": "",  # 文案编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_giftPromotion_queryGiftCardTextPage(data=data, headers=headers):
    """
    送礼贺卡文案分页列表查询
    /mgmt/cms/giftPromotion/queryGiftCardTextPage

    参数说明:
    - createTimeEnd: 创建时间范围结束
    - createTimeStart: 创建时间范围开始
    - giftCardText: 文案内容
    - pageNum: 页码
    - pageSize: 每页页数
    - textNo: 文案编号
    """

    url = "/mgmt/cms/giftPromotion/queryGiftCardTextPage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
