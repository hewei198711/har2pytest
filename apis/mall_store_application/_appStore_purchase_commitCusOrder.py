import os

from util.client import client

data = {
    "isDelivery": 0,  # 店铺中心无需填写  0不需要发货 1需要发货
    "orderRemarks": "",  # 备注 店铺中心无需填写
    "productList": [],  # 押货列表
    "storeCode": "",  # 服务中心编码
    "transId": "",  # 业务id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchase_commitCusOrder(data=data, headers=headers):
    """
    提交定制品押货单
    /appStore/purchase/commitCusOrder

    参数说明:
    - isDelivery: 店铺中心无需填写  0不需要发货 1需要发货
    - orderRemarks: 备注 店铺中心无需填写
    - productList: 押货列表
    - storeCode: 服务中心编码
    - transId: 业务id
    """

    url = "/appStore/purchase/commitCusOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
