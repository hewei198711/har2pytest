import os

from util.client import client

params = {
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "productCode": "",  # 商品编号
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_order_listNotDeliverProduct(params=params, headers=headers):
    """
    后台获取欠货未发列表
    /mgmt/inventory/order/listNotDeliverProduct

    参数说明:
    - pageNum: 页数
    - pageSize: 页大小
    - productCode: 商品编号
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/order/listNotDeliverProduct"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
