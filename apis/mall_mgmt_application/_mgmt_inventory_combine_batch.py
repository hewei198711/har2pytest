import os

from util.client import client

data = {
    "combineIds": [],  # 套装组合id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_combine_batch(data=data, headers=headers):
    """
    批量套装组合
    /mgmt/inventory/combine/batch

    参数说明:
    - combineIds: 套装组合id
    """

    url = "/mgmt/inventory/combine/batch"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
