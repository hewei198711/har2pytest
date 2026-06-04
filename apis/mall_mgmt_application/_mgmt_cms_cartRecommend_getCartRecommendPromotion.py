import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_cartRecommend_getCartRecommendPromotion(headers=headers):
    """
    查询购物车推荐活动
    /mgmt/cms/cartRecommend/getCartRecommendPromotion
    """

    url = "/mgmt/cms/cartRecommend/getCartRecommendPromotion"
    with client.get(url=url, headers=headers) as r:
        return r
