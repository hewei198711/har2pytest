import os

from util.client import client

params = {
    "deliverSnList": [],  # 发货单号列表
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_diffOrder_searchProductsByDeliverSnList(params=params, headers=headers):
    """
    查询对应发货单的所有商品
    /mgmt/inventory/dis/mortgage/diffOrder/searchProductsByDeliverSnList

    参数说明:
    - deliverSnList: 发货单号列表
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/dis/mortgage/diffOrder/searchProductsByDeliverSnList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
