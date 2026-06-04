import os

from util.client import client

data = {
    "promotionLabelUrl": "",  # 活动标签图片
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_cartRecommend_savePromotionLabel(data=data, headers=headers):
    """
    保存购物车推荐活动标签
    /mgmt/cms/cartRecommend/savePromotionLabel

    参数说明:
    - promotionLabelUrl: 活动标签图片
    """

    url = "/mgmt/cms/cartRecommend/savePromotionLabel"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
