import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseOrder_getNegateCusProductsForWebAddPage(headers=headers):
    """
    提交定制押货单页面的负库存押货商品列表
    /appStore/purchaseOrder/getNegateCusProductsForWebAddPage
    """

    url = "/appStore/purchaseOrder/getNegateCusProductsForWebAddPage"
    with client.get(url=url, headers=headers) as r:
        return r
