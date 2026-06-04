import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_cartRecommend_delPromotionLabel(data=data, headers=headers):
    """
    删除购物车推荐活动标签
    /mgmt/cms/cartRecommend/delPromotionLabel

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/cartRecommend/delPromotionLabel"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
