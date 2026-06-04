import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_getStatisticsOrderType(headers=headers):
    """
    运营后台各系列产品业绩统计表产品类型
    /mgmt/order/getStatisticsOrderType
    """

    url = "/mgmt/order/getStatisticsOrderType"
    with client.get(url=url, headers=headers) as r:
        return r
