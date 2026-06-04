import os

from util.client import client

params = {
    "keyword": "",  # 一或二级商品关键字
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_order_getCusProductsForOpAddPage(params=params, headers=headers):
    """
    运营后台提交定制品押货单页面的押货商品搜索列表
    /mgmt/inventory/order/getCusProductsForOpAddPage

    参数说明:
    - keyword: 一或二级商品关键字
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/order/getCusProductsForOpAddPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
