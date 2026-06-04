import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_return_config_exportDetailConfig(params=params, headers=headers):
    """
    根据id查询详情导出excel
    /mgmt/inventory/return/config/exportDetailConfig

    参数说明:
    - id: id
    """

    url = "/mgmt/inventory/return/config/exportDetailConfig"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
