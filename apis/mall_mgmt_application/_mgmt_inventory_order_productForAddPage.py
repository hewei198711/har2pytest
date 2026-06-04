import os

from util.client import client

params = {
    "productCode": "",  # productCode
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_order_productForAddPage(params=params, headers=headers):
    """
    新增押货单页面:根据产品编码获取
    /mgmt/inventory/order/productForAddPage

    参数说明:
    - productCode: productCode
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/order/productForAddPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
