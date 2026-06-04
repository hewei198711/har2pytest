import os

from util.client import client

params = {
    "storeCode": "",  # 店铺编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_returnOrder_searchPositiveProducts(params=params, headers=headers):
    """
    获取服务中心正库存的商品信息
    /mgmt/inventory/dis/mortgage/returnOrder/searchPositiveProducts

    参数说明:
    - storeCode: 店铺编号
    """

    url = "/mgmt/inventory/dis/mortgage/returnOrder/searchPositiveProducts"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
