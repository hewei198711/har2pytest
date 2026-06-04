import os

from util.client import client

data = {
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "queryMonthBegin": "",  # 查询开始月份，格式：yyyyMM
    "queryMonthEnd": "",  # 查询结束月份，格式：yyyyMM
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_invoiceConfigList(data=data, headers=headers):
    """
    查询订单发票配置日志列表
    /mgmt/order/invoiceConfigList

    参数说明:
    - pageNum: 页数
    - pageSize: 每页显示数
    - queryMonthBegin: 查询开始月份，格式：yyyyMM
    - queryMonthEnd: 查询结束月份，格式：yyyyMM
    """

    url = "/mgmt/order/invoiceConfigList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
