import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_recommend_getRecommend(headers=headers):
    """
    获取推荐商品列表
    /mgmt/cms/recommend/getRecommend
    """

    url = "/mgmt/cms/recommend/getRecommend"
    with client.get(url=url, headers=headers) as r:
        return r
