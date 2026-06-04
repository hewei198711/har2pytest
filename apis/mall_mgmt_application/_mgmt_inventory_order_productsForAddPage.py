import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_order_productsForAddPage(params=params, headers=headers):
    """
    新增押货单页面:获取服务中心的全部库存信息
    /mgmt/inventory/order/productsForAddPage

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/order/productsForAddPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
