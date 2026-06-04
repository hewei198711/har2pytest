import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_combine_detail_export(params=params, headers=headers):
    """
    套装组合明细导出
    /mgmt/inventory/combine/detail/export

    参数说明:
    - id: id
    """

    url = "/mgmt/inventory/combine/detail/export"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
