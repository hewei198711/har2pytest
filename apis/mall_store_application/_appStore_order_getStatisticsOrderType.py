import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_getStatisticsOrderType(headers=headers):
    """
    各系列产品业绩统计表产品类型
    /appStore/order/getStatisticsOrderType
    """

    url = "/appStore/order/getStatisticsOrderType"
    with client.get(url=url, headers=headers) as r:
        return r
