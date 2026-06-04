import os

from util.client import client

params = {
    "key": "",  # key
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_group_order_sample_url(params=params, headers=headers):
    """
    获取团购单模板路径
    /mgmt/inventory/group-order/sample-url

    参数说明:
    - key: key
    """

    url = "/mgmt/inventory/group-order/sample-url"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
