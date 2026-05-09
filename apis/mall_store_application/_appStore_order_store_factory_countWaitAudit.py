import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_store_factory_countWaitAudit(headers=headers):
    """
    统计待审核返厂维修单
    /appStore/order/store/factory/countWaitAudit
    """

    url = "/appStore/order/store/factory/countWaitAudit"
    with client.get(url=url, headers=headers) as r:
        return r
