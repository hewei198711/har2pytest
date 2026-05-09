import os

from util.client import client

data = {
    "isDelivery": False,  # 是否发货
    "orderRemark": "",  # 押货单备注
    "productList": [],  # 押货单商品列表信息
    "storeCode": "",  # 服务中心编码
    "transId": "",  # 业务id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgageOrder_mortgage(data=data, headers=headers):
    """
    押货下单
    /appStore/store/dis/mortgageOrder/mortgage

    参数说明:
    - isDelivery: 是否发货
    - orderRemark: 押货单备注
    - productList: 押货单商品列表信息
    - storeCode: 服务中心编码
    - transId: 业务id
    """

    url = "/appStore/store/dis/mortgageOrder/mortgage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
