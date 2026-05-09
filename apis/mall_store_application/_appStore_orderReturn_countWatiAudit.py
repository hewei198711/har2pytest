import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_orderReturn_countWatiAudit(headers=headers):
    """
    统计门店自提待审核的退货单
    /appStore/orderReturn/countWatiAudit
    """

    url = "/appStore/orderReturn/countWatiAudit"
    with client.get(url=url, headers=headers) as r:
        return r
