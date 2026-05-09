import os

from util.client import client

params = {
    "maxMonth": 0,  # 月份最大值，月份格式：yyyyMM
    "minMonth": 0,  # 月份最小值，月份格式：yyyyMM
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "product": "",  # 产品编码或产品名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_dis_inventory_bill_print(params=params, headers=headers):
    """
    打印库存对账单
    /appStore/dis-inventory/bill/print

    参数说明:
    - maxMonth: 月份最大值，月份格式：yyyyMM
    - minMonth: 月份最小值，月份格式：yyyyMM
    - pageNum: 页数
    - pageSize: 页大小
    - product: 产品编码或产品名称
    """

    url = "/appStore/dis-inventory/bill/print"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
