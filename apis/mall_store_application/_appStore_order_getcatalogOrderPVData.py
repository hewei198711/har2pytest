import os

from util.client import client

params = {
    "orderMonth": "",  # 业绩月分
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_getcatalogOrderPVData(params=params, headers=headers):
    """
    85折订单分类pv统计
    /appStore/order/getcatalogOrderPVData

    参数说明:
    - orderMonth: 业绩月分
    - storeCode: 服务中心编号
    """

    url = "/appStore/order/getcatalogOrderPVData"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
