import os

from util.client import client

data = {
    "serialNoList": [],  # 关联的产品编码列表
    "targetValue": "",  # 所有单值的关联内容：抽奖/随心购活动id、问卷key、内外部链接
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_cartRecommend_saveCartRecommendProduct(data=data, headers=headers):
    """
    保存购物车推荐产品
    /mgmt/cms/cartRecommend/saveCartRecommendProduct

    参数说明:
    - serialNoList: 关联的产品编码列表
    - targetValue: 所有单值的关联内容：抽奖/随心购活动id、问卷key、内外部链接
    """

    url = "/mgmt/cms/cartRecommend/saveCartRecommendProduct"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
