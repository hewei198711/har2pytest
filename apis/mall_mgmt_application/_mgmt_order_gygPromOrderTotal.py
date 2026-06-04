import os

from util.client import client

data = {
    "payEndTime": "",  # 支付结束时间，格式：yyyy-MM-dd
    "payStartTime": "",  # 支付开始时间，格式：yyyy-MM-dd
    "promotionId": 0,  # 活动id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_gygPromOrderTotal(data=data, headers=headers):
    """
    公益购活动详情-订单数据统计
    /mgmt/order/gygPromOrderTotal

    参数说明:
    - payEndTime: 支付结束时间，格式：yyyy-MM-dd
    - payStartTime: 支付开始时间，格式：yyyy-MM-dd
    - promotionId: 活动id
    """

    url = "/mgmt/order/gygPromOrderTotal"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
