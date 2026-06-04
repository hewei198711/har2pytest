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


def _mgmt_dis_inventory_productStockGtZero(params=params, headers=headers):
    """
    获取库存不为0的商品信息
    /mgmt/dis-inventory/productStockGtZero

    参数说明:
    - productCode: productCode
    - storeCode: storeCode
    """

    url = "/mgmt/dis-inventory/productStockGtZero"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
