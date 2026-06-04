import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_cartRecommend_getPromotionLabelList(headers=headers):
    """
    获取购物车推荐活动标签列表
    /mgmt/cms/cartRecommend/getPromotionLabelList
    """

    url = "/mgmt/cms/cartRecommend/getPromotionLabelList"
    with client.get(url=url, headers=headers) as r:
        return r
