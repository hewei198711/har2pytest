import os

from util.client import client

data = {
    "customerCard": "",  # 顾客卡号
    "customerName": "",  # 顾客姓名
    "customerPhone": "",  # 顾客手机号
    "endPayTime": "",  # 领取-结束时间
    "orderNo": "",  # 领取单编号
    "orderStatus": 0,  # 订单状态  2->待发货 3->待收货 99->已完成
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 页面大小
    "serialNo": "",  # 赠品编码
    "startPayTime": "",  # 领取-开始时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_orderGift_queryGiftOrderList(data=data, headers=headers):
    """
    赠品领取单管理-列表
    /mgmt/orderGift/queryGiftOrderList

    参数说明:
    - customerCard: 顾客卡号
    - customerName: 顾客姓名
    - customerPhone: 顾客手机号
    - endPayTime: 领取-结束时间
    - orderNo: 领取单编号
    - orderStatus: 订单状态  2->待发货 3->待收货 99->已完成
    - pageNum: 页码
    - pageSize: 页面大小
    - serialNo: 赠品编码
    - startPayTime: 领取-开始时间
    """

    url = "/mgmt/orderGift/queryGiftOrderList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
