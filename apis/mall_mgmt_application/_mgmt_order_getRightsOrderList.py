import os

from util.client import client

params = {
    "beginPayTime": "",  # 兑换开始时间
    "customerCard": "",  # 顾客会员卡
    "customerName": "",  # 顾客姓名
    "customerPhone": "",  # 注册手机号
    "endPayTime": "",  # 兑换结束时间
    "from": 0,  # TODO: 添加参数说明
    "orderNo": "",  # 订单编号/兑换流水号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "serialNo": "",  # 产品编码
    "title": "",  # 产品名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_getRightsOrderList(params=params, headers=headers):
    """
    查询用户权益订单列表
    /mgmt/order/getRightsOrderList

    参数说明:
    - beginPayTime: 兑换开始时间
    - customerCard: 顾客会员卡
    - customerName: 顾客姓名
    - customerPhone: 注册手机号
    - endPayTime: 兑换结束时间
    - orderNo: 订单编号/兑换流水号
    - pageNum: 页数
    - pageSize: 每页显示数
    - serialNo: 产品编码
    - title: 产品名称
    """

    url = "/mgmt/order/getRightsOrderList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
