import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_exchangeOrder_searchAuditInfo(headers=headers):
    """
    展示审批保存信息
    /mgmt/inventory/dis/mortgage/exchangeOrder/searchAuditInfo
    """

    url = "/mgmt/inventory/dis/mortgage/exchangeOrder/searchAuditInfo"
    with client.get(url=url, headers=headers) as r:
        return r
