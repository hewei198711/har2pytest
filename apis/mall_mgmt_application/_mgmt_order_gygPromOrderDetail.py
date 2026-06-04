import os

from util.client import client

data = {
    "from": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "payEndTime": "",  # 支付结束时间，格式：yyyy-MM-dd
    "payStartTime": "",  # 支付开始时间，格式：yyyy-MM-dd
    "promotionId": 0,  # 活动id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_gygPromOrderDetail(data=data, headers=headers):
    """
    公益购活动详情-订单数据明细
    /mgmt/order/gygPromOrderDetail

    参数说明:
    - pageNum: 页数
    - pageSize: 每页显示数
    - payEndTime: 支付结束时间，格式：yyyy-MM-dd
    - payStartTime: 支付开始时间，格式：yyyy-MM-dd
    - promotionId: 活动id
    """

    url = "/mgmt/order/gygPromOrderDetail"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
