import os

from util.client import client

data = {
    "signEndTime": "",  # 签约结束月份
    "signStartTime": "",  # 签约开始月份
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_orderSign_signRanking(data=data, headers=headers):
    """
    店铺系统-时光荟签约购排名榜
    /appStore/order/orderSign/signRanking

    参数说明:
    - signEndTime: 签约结束月份
    - signStartTime: 签约开始月份
    - storeCode: 服务中心编号
    """

    url = "/appStore/order/orderSign/signRanking"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
