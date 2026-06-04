import os

from util.client import client

params = {
    "keyword": "",  # keyword
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_order_searchProductsForAddPage(params=params, headers=headers):
    """
    新增押货单页面:根据产品关键字搜索普通商品列表
    /mgmt/inventory/order/searchProductsForAddPage

    参数说明:
    - keyword: keyword
    - pageNum: pageNum
    - pageSize: pageSize
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/order/searchProductsForAddPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
