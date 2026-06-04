import os

from util.client import client

params = {
    "endTime": "",  # 结束时间
    "from": 0,  # TODO: 添加参数说明
    "operator": "",  # 操作人
    "optType": 0,  # 操作类型，1->代开发票，2->重开发票，3->隔月开票审核
    "orderNo": "",  # 订单编号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "startTime": "",  # 开始时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_getInvoiceOptLogList(params=params, headers=headers):
    """
    运营后台-获取发票操作记录列表
    /mgmt/order/getInvoiceOptLogList

    参数说明:
    - endTime: 结束时间
    - operator: 操作人
    - optType: 操作类型，1->代开发票，2->重开发票，3->隔月开票审核
    - orderNo: 订单编号
    - pageNum: 页数
    - pageSize: 每页显示数
    - startTime: 开始时间
    """

    url = "/mgmt/order/getInvoiceOptLogList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
