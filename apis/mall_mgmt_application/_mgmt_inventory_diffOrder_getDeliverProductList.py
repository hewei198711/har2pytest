import os

from util.client import client

params = {
    "deliverSnList": [],  # 发货单编号 多个用逗号','隔开
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_diffOrder_getDeliverProductList(params=params, headers=headers):
    """
    获取发货单列表对应的商品
    /mgmt/inventory/diffOrder/getDeliverProductList

    参数说明:
    - deliverSnList: 发货单编号 多个用逗号','隔开
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/diffOrder/getDeliverProductList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
