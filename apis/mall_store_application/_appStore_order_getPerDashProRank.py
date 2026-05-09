import os

from util.client import client

data = {
    "endMonth": "",  # 结束月，格式：yyyyMM
    "startMonth": "",  # 开始月，格式：yyyyMM
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_getPerDashProRank(data=data, headers=headers):
    """
    业绩看板-商品排行榜TOP20
    /appStore/order/getPerDashProRank

    参数说明:
    - endMonth: 结束月，格式：yyyyMM
    - startMonth: 开始月，格式：yyyyMM
    - storeCode: 服务中心编号
    """

    url = "/appStore/order/getPerDashProRank"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
