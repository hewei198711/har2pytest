import os

from util.client import client

data = {
    "orderNo": "",  # 订单号
    "ownerCard": "",  # 送货人卡号
    "ownerId": 0,  # 送货人id
    "ownerName": "",  # 送货人姓名
    "ownerPhone": "",  # 送货人手机
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_updateOwnerInfo(data=data, headers=headers):
    """
    修改订单送货人信息
    /mgmt/order/updateOwnerInfo

    参数说明:
    - orderNo: 订单号
    - ownerCard: 送货人卡号
    - ownerId: 送货人id
    - ownerName: 送货人姓名
    - ownerPhone: 送货人手机
    """

    url = "/mgmt/order/updateOwnerInfo"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
