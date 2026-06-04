import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_combine_show(params=params, headers=headers):
    """
    套装组合展示
    /mgmt/inventory/combine/show

    参数说明:
    - id: id
    """

    url = "/mgmt/inventory/combine/show"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
