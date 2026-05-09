import os

from util.client import client

params = {
    "beginTime": 0,  # 开始时间，月份格式：yyyyMM
    "endTime": 0,  # 结束时间，月份格式：yyyyMM
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "product": "",  # 产品编码或产品名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_inventory_printStockBill(params=params, headers=headers):
    """
    打印库存对账单
    /appStore/inventory/printStockBill

    参数说明:
    - beginTime: 开始时间，月份格式：yyyyMM
    - endTime: 结束时间，月份格式：yyyyMM
    - pageNum: 页数
    - pageSize: 页大小
    - product: 产品编码或产品名称
    """

    url = "/appStore/inventory/printStockBill"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
