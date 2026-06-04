import os

from util.client import client

data = {
    "address": {
        "address": "",
        "city": "",
        "cityCode": "",
        "district": "",
        "districtCode": "",
        "postCode": "",
        "province": "",
        "provinceCode": "",
        "storeCode": "",
        "storeName": "",
        "storePhone": "",
        "street": "",
        "streetCode": "",
    },  # 收货地址信息
    "orderNo": "",  # 订单号
    "receiver": "",  # 收货人
    "receiverPhone": "",  # 收货人电话
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_updateReceiverInfo(data=data, headers=headers):
    """
    修改订单收货人信息
    /mgmt/order/updateReceiverInfo

    参数说明:
    - address: 收货地址信息
    - orderNo: 订单号
    - receiver: 收货人
    - receiverPhone: 收货人电话
    """

    url = "/mgmt/order/updateReceiverInfo"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
