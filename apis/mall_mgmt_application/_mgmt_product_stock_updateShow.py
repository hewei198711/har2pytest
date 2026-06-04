import os

from util.client import client

data = {
    "historyId": 0,  # 库存版本id
    "isShowStock": 0,  # 是否展示库存量 0-否，1-是
    "stockId": 0,  # 库存id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_stock_updateShow(data=data, headers=headers):
    """
    配置是否显示库存量
    /mgmt/product/stock/updateShow

    参数说明:
    - historyId: 库存版本id
    - isShowStock: 是否展示库存量 0-否，1-是
    - stockId: 库存id
    """

    url = "/mgmt/product/stock/updateShow"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
