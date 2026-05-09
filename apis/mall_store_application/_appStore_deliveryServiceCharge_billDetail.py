import os

from util.client import client

params = {
    "month": "",  # 月份
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_deliveryServiceCharge_billDetail(params=params, headers=headers):
    """
    配送服务费扣补明细
    /appStore/deliveryServiceCharge/billDetail

    参数说明:
    - month: 月份
    - pageNum: 页数
    - pageSize: 页大小
    """

    url = "/appStore/deliveryServiceCharge/billDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
