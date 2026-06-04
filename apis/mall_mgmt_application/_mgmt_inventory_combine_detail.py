import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_combine_detail(params=params, headers=headers):
    """
    查询套装组合明细
    /mgmt/inventory/combine/detail

    参数说明:
    - id: id
    """

    url = "/mgmt/inventory/combine/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
