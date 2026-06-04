import os

from util.client import client

data = {
    "deliverTime": "",  # 发货时间
    "deliverType": 0,  # 发货方式 1顾客自提 2邮寄
    "expressCompany": "",  # 新品配送物流公司
    "expressNo": "",  # 物流单号
    "orderId": 0,  # 换货单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_exchangeOrder_deliver(data=data, headers=headers):
    """
    发货
    /mgmt/inventory/dis/mortgage/exchangeOrder/deliver

    参数说明:
    - deliverTime: 发货时间
    - deliverType: 发货方式 1顾客自提 2邮寄
    - expressCompany: 新品配送物流公司
    - expressNo: 物流单号
    - orderId: 换货单id
    """

    url = "/mgmt/inventory/dis/mortgage/exchangeOrder/deliver"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
