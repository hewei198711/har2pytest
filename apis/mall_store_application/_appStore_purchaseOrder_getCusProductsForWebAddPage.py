import os

from util.client import client

params = {
    "keyword": "",  # 一或二级商品关键字
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseOrder_getCusProductsForWebAddPage(params=params, headers=headers):
    """
    提交定制品押货单页面的押货商品搜索列表
    /appStore/purchaseOrder/getCusProductsForWebAddPage

    参数说明:
    - keyword: 一或二级商品关键字
    """

    url = "/appStore/purchaseOrder/getCusProductsForWebAddPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
