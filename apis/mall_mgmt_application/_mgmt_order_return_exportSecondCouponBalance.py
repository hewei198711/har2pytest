import os

from util.client import client

data = {
    "creatorCard": "",  # 开单人卡号
    "customerCard": "",  # 购货人卡号
    "from": 0,  # TODO: 添加参数说明
    "orderCompleteTimeBegin": "",  # 订单完成开始时间 #格式yyyy-MM-dd
    "orderCompleteTimeEnd": "",  # 订单完成结束时间 #格式yyyy-MM-dd
    "orderNo": "",  # 订单编号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "returnCompleteTimeBegin": "",  # 退货完成开始时间 #格式yyyy-MM-dd
    "returnCompleteTimeEnd": "",  # 退货完成结束时间 #格式yyyy-MM-dd
    "returnNo": "",  # 退货单号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_return_exportSecondCouponBalance(data=data, headers=headers):
    """
    导出秒返券差额表记录
    /mgmt/order/return/exportSecondCouponBalance

    参数说明:
    - creatorCard: 开单人卡号
    - customerCard: 购货人卡号
    - orderCompleteTimeBegin: 订单完成开始时间 #格式yyyy-MM-dd
    - orderCompleteTimeEnd: 订单完成结束时间 #格式yyyy-MM-dd
    - orderNo: 订单编号
    - pageNum: 页数
    - pageSize: 每页显示数
    - returnCompleteTimeBegin: 退货完成开始时间 #格式yyyy-MM-dd
    - returnCompleteTimeEnd: 退货完成结束时间 #格式yyyy-MM-dd
    - returnNo: 退货单号
    """

    url = "/mgmt/order/return/exportSecondCouponBalance"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
