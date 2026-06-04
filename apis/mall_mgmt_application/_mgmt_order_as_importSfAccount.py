import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_order_as_importSfAccount(headers=headers):
    """
    顺丰上门取件对账单-导入
    /mgmt/order/as/importSfAccount
    """

    url = "/mgmt/order/as/importSfAccount"
    with client.post(url=url, headers=headers) as r:
        return r
