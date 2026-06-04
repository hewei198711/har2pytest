import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_returnOrder_searchAuditInfo(headers=headers):
    """
    展示审批保存信息
    /mgmt/inventory/dis/mortgage/returnOrder/searchAuditInfo
    """

    url = "/mgmt/inventory/dis/mortgage/returnOrder/searchAuditInfo"
    with client.get(url=url, headers=headers) as r:
        return r
