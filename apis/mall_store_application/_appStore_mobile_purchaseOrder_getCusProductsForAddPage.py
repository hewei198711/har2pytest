import os

from util.client import client

params = {
    "allowNegateStock": 0,  # 是否允许返回负库存 0否 1是
    "keyword": "",  # 一级商品关键字
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_purchaseOrder_getCusProductsForAddPage(params=params, headers=headers):
    """
    APP提交定制品押货单页面的一级押货商品搜索
    /appStore/mobile/purchaseOrder/getCusProductsForAddPage

    参数说明:
    - allowNegateStock: 是否允许返回负库存 0否 1是
    - keyword: 一级商品关键字
    - pageNum: 页数
    - pageSize: 页大小
    """

    url = "/appStore/mobile/purchaseOrder/getCusProductsForAddPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
