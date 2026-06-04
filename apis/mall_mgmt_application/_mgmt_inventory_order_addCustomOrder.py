import os

from util.client import client

data = {
    "isDelivery": 0,  # 店铺中心无需填写  0不需要发货 1需要发货
    "orderRemarks": "",  # 备注 店铺中心无需填写
    "productList": [
        {"productCode": "", "productMortgagePrice": 0.0, "productNum": 0, "productSecondCode": ""}
    ],  # 押货列表
    "storeCode": "",  # 服务中心编码
    "transId": "",  # 业务id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_order_addCustomOrder(data=data, headers=headers):
    """
    添加定制品押货单
    /mgmt/inventory/order/addCustomOrder

    参数说明:
    - isDelivery: 店铺中心无需填写  0不需要发货 1需要发货
    - orderRemarks: 备注 店铺中心无需填写
    - productList: 押货列表
    - productList.productCode: 押货商品编码
    - productList.productMortgagePrice: 商品押货价
    - productList.productNum: 押货商品数量
    - productList.productSecondCode: 押货商品二级编码
    - storeCode: 服务中心编码
    - transId: 业务id
    """

    url = "/mgmt/inventory/order/addCustomOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
