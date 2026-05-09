import os

from util.client import client

data = {
    "isDelivery": False,  # 是否发货
    "orderId": 0,  # 押货单id
    "orderRemark": "",  # 押货单备注
    "productList": [],  # 押货单商品列表信息
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgageOrder_edit(data=data, headers=headers):
    """
    押货单编辑
    /appStore/store/dis/mortgageOrder/edit

    参数说明:
    - isDelivery: 是否发货
    - orderId: 押货单id
    - orderRemark: 押货单备注
    - productList: 押货单商品列表信息
    """

    url = "/appStore/store/dis/mortgageOrder/edit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
