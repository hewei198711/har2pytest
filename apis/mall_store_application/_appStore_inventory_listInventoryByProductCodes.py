import os

from util.client import client

params = {
    "productCodes": [],  # 商品编码列表
    "storeCode": "",  # 店铺编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_inventory_listInventoryByProductCodes(params=params, headers=headers):
    """
    商品编码查询库存(自动按当前店铺的经营模式去查询)
    /appStore/inventory/listInventoryByProductCodes

    参数说明:
    - productCodes: 商品编码列表
    - storeCode: 店铺编码
    """

    url = "/appStore/inventory/listInventoryByProductCodes"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
