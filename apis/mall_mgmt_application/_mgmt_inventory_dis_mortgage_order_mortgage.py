import os

from util.client import client

data = {
    "isDelivery": False,  # 是否发货
    "orderRemark": "",  # 押货单备注
    "productList": [{"mortgageNum": 0, "mortgagePrice": 0.0, "productCode": ""}],  # 押货单商品列表信息
    "storeCode": "",  # 服务中心编码
    "transId": "",  # 业务id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_order_mortgage(data=data, headers=headers):
    """
    押货下单
    /mgmt/inventory/dis/mortgage/order/mortgage

    参数说明:
    - isDelivery: 是否发货
    - orderRemark: 押货单备注
    - productList: 押货单商品列表信息
    - productList.mortgageNum: 押货商品数量
    - productList.mortgagePrice: 商品押货价
    - productList.productCode: 押货商品编码
    - storeCode: 服务中心编码
    - transId: 业务id
    """

    url = "/mgmt/inventory/dis/mortgage/order/mortgage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
