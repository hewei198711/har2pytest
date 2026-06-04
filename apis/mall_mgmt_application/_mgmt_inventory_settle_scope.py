import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_settle_scope(headers=headers):
    """
    获取月结时间范围
    /mgmt/inventory/settle-scope
    """

    url = "/mgmt/inventory/settle-scope"
    with client.get(url=url, headers=headers) as r:
        return r
