import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_order_getNegateCusProductsForOpAddPage(params=params, headers=headers):
    """
    运营后台添加定制品押货单页面的负库存商品列表
    /mgmt/inventory/order/getNegateCusProductsForOpAddPage

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/order/getNegateCusProductsForOpAddPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
