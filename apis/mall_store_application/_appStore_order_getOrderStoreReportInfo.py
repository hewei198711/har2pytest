import os
from urllib.parse import urlencode

from util.client import client

data = {
    "type": "",  # 类型：1、享受服务费的订单汇总，2、各系列产品业绩统计表
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _appStore_order_getOrderStoreReportInfo(data=data, headers=headers):
    """
    查询店铺订单报表信息
    /appStore/order/getOrderStoreReportInfo

    参数说明:
    - type: 类型：1、享受服务费的订单汇总，2、各系列产品业绩统计表
    """

    url = "/appStore/order/getOrderStoreReportInfo"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
