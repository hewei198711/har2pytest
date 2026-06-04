import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disManageModelChange_getDetailById(params=params, headers=headers):
    """
    记录详情
    /mgmt/inventory/disManageModelChange/getDetailById

    参数说明:
    - id: id
    """

    url = "/mgmt/inventory/disManageModelChange/getDetailById"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
