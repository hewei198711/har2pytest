import os

from util.client import client

data = {
    "customerCard": "",  # 顾客卡号
    "customerName": "",  # 顾客姓名
    "customerPhone": "",  # 顾客手机号
    "customerType": 0,  # 顾客类型 1->普通顾客 2->优惠顾客 3->云商 4->微店
    "energyRangeEnd": 0.0,  # 能量范围，结束值
    "energyRangeStart": 0.0,  # 能量范围，开始值
    "from": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "payEndTime": "",  # 支付结束时间，格式：yyyy-MM
    "payStartTime": "",  # 支付开始时间，格式：yyyy-MM
    "promotionId": 0,  # 活动id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_gygPromCustomerDetail(data=data, headers=headers):
    """
    公益购活动详情-顾客数据情况
    /mgmt/order/gygPromCustomerDetail

    参数说明:
    - customerCard: 顾客卡号
    - customerName: 顾客姓名
    - customerPhone: 顾客手机号
    - customerType: 顾客类型 1->普通顾客 2->优惠顾客 3->云商 4->微店
    - energyRangeEnd: 能量范围，结束值
    - energyRangeStart: 能量范围，开始值
    - pageNum: 页数
    - pageSize: 每页显示数
    - payEndTime: 支付结束时间，格式：yyyy-MM
    - payStartTime: 支付开始时间，格式：yyyy-MM
    - promotionId: 活动id
    """

    url = "/mgmt/order/gygPromCustomerDetail"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
