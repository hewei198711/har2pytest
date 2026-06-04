import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_order_as_unmatchedSfBillExport(headers=headers):
    """
    导出未匹配的顺丰对账单
    /mgmt/order/as/unmatchedSfBillExport
    """

    url = "/mgmt/order/as/unmatchedSfBillExport"
    with client.post(url=url, headers=headers) as r:
        return r
