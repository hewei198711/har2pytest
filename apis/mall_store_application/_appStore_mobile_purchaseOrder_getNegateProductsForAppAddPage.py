import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_purchaseOrder_getNegateProductsForAppAddPage(headers=headers):
    """
    APP服务中心提交押货单页面的负库存押货商品列表(包括押货车缓存)
    /appStore/mobile/purchaseOrder/getNegateProductsForAppAddPage
    """

    url = "/appStore/mobile/purchaseOrder/getNegateProductsForAppAddPage"
    with client.get(url=url, headers=headers) as r:
        return r
