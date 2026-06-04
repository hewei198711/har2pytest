import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_settled_scope(headers=headers):
    """
    获取月结完成时间范围
    /mgmt/inventory/settled-scope
    """

    url = "/mgmt/inventory/settled-scope"
    with client.get(url=url, headers=headers) as r:
        return r
