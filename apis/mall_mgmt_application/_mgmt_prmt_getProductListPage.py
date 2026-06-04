import os

from util.client import client

params = {
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
    "product": "",  # product
    "promotionId": 0,  # promotionId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_getProductListPage(params=params, headers=headers):
    """
    分页获取活动产品(详情)
    /mgmt/prmt/getProductListPage

    参数说明:
    - pageNum: pageNum
    - pageSize: pageSize
    - product: product
    - promotionId: promotionId
    """

    url = "/mgmt/prmt/getProductListPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
