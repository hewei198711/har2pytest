import os

from util.client import client

params = {
    "keyword": "",  # 商品关键字
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "storeCode": "",  # 店铺编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_inventory_pageInventoryByKeyword(params=params, headers=headers):
    """
    关键字查询库存(自动按当前店铺的经营模式去查询)
    /appStore/inventory/pageInventoryByKeyword

    参数说明:
    - keyword: 商品关键字
    - pageNum: 页数
    - pageSize: 页大小
    - storeCode: 店铺编码
    """

    url = "/appStore/inventory/pageInventoryByKeyword"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
