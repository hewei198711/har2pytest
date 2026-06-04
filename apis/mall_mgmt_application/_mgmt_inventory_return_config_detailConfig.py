import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_return_config_detailConfig(params=params, headers=headers):
    """
    根据id查询详情
    /mgmt/inventory/return/config/detailConfig

    参数说明:
    - id: id
    """

    url = "/mgmt/inventory/return/config/detailConfig"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
