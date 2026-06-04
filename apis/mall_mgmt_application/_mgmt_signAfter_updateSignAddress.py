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
    "receiver": "",  # 收货人
    "receiverPhone": "",  # 收货人电话
    "signNo": "",  # 签约单号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_signAfter_updateSignAddress(data=data, headers=headers):
    """
    签约购修改收货地址
    /mgmt/signAfter/updateSignAddress

    参数说明:
    - address: 收货地址信息
    - receiver: 收货人
    - receiverPhone: 收货人电话
    - signNo: 签约单号
    """

    url = "/mgmt/signAfter/updateSignAddress"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
