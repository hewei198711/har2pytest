import os

from util.client import client

params = {
    "type": 0,  # type
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_common_getReason(params=params, headers=headers):
    """
    获取各种退换货原因
    /mgmt/inventory/common/getReason

    参数说明:
    - type: type
    """

    url = "/mgmt/inventory/common/getReason"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
