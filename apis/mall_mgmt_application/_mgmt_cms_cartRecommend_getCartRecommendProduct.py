import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_cartRecommend_getCartRecommendProduct(headers=headers):
    """
    查询购物车推荐产品
    /mgmt/cms/cartRecommend/getCartRecommendProduct
    """

    url = "/mgmt/cms/cartRecommend/getCartRecommendProduct"
    with client.get(url=url, headers=headers) as r:
        return r
