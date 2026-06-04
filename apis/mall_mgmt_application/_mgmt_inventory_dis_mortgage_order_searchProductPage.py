import os

from util.client import client

params = {
    "keyword": "",  # 关键字
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "storeCode": "",  # 店铺编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_order_searchProductPage(params=params, headers=headers):
    """
    关键字搜索可押货商品分页
    /mgmt/inventory/dis/mortgage/order/searchProductPage

    参数说明:
    - keyword: 关键字
    - pageNum: 页数
    - pageSize: 页大小
    - storeCode: 店铺编号
    """

    url = "/mgmt/inventory/dis/mortgage/order/searchProductPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
