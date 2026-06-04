import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_inventory_returnOrder_autoDealReturnTest(headers=headers):
    """
    押货退货过期自动取消 (测试用)
    /mgmt/inventory/returnOrder/autoDealReturnTest
    """

    url = "/mgmt/inventory/returnOrder/autoDealReturnTest"
    with client.post(url=url, headers=headers) as r:
        return r
