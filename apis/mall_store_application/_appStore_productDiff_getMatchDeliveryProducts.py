import os

from util.client import client

params = {
    "deliverSnList": [],  # 发货单号列表,多个用逗号隔开
    "keyword": "",  # 产品编码or名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_productDiff_getMatchDeliveryProducts(params=params, headers=headers):
    """
    根据产品编码or名称模糊搜索发货单的商品
    /appStore/productDiff/getMatchDeliveryProducts

    参数说明:
    - deliverSnList: 发货单号列表,多个用逗号隔开
    - keyword: 产品编码or名称
    """

    url = "/appStore/productDiff/getMatchDeliveryProducts"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
