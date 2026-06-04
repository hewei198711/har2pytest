import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_inventory_exchangeOrder_autoDealReturnTest(headers=headers):
    """
    押货换货过期自动处理未退货的押货单 (测试用)
    /mgmt/inventory/exchangeOrder/autoDealReturnTest
    """

    url = "/mgmt/inventory/exchangeOrder/autoDealReturnTest"
    with client.post(url=url, headers=headers) as r:
        return r
