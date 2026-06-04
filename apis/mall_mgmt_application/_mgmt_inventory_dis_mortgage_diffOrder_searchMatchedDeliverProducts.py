import os

from util.client import client

params = {
    "deliverSnList": [],  # 发货单编号列表
    "keyword": "",  # 产品编码or名称
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_diffOrder_searchMatchedDeliverProducts(params=params, headers=headers):
    """
    根据产品编码or名称模糊搜索发货单的商品
    /mgmt/inventory/dis/mortgage/diffOrder/searchMatchedDeliverProducts

    参数说明:
    - deliverSnList: 发货单编号列表
    - keyword: 产品编码or名称
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/dis/mortgage/diffOrder/searchMatchedDeliverProducts"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
