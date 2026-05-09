import os

from util.client import client

params = {
    "deliverSnList": [],  # 发货单编号列表
    "keyword": "",  # 产品编码or名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_diffOrder_searchMatchedDeliverProducts(params=params, headers=headers):
    """
    根据产品编码or名称模糊搜索发货单的商品
    /appStore/store/dis/mortgage/diffOrder/searchMatchedDeliverProducts

    参数说明:
    - deliverSnList: 发货单编号列表
    - keyword: 产品编码or名称
    """

    url = "/appStore/store/dis/mortgage/diffOrder/searchMatchedDeliverProducts"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
