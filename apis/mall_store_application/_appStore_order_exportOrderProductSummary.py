import os

from util.client import client

params = {
    "orderMonth": "",  # 业绩月份
    "orderMonths": [],  # 业绩月份数组
    "storeCode": "",  # 店铺编码
    "storeName": "",  # 店铺名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_exportOrderProductSummary(params=params, headers=headers):
    """
    各系列产品业绩统计汇总表导出
    /appStore/order/exportOrderProductSummary

    参数说明:
    - orderMonth: 业绩月份
    - orderMonths: 业绩月份数组
    - storeCode: 店铺编码
    - storeName: 店铺名称
    """

    url = "/appStore/order/exportOrderProductSummary"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
