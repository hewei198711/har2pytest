import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_distribution_delDistribution(params=params, headers=headers):
    """
    服务中心分配量删除
    /mgmt/inventory/distribution/delDistribution

    参数说明:
    - id: id
    """

    url = "/mgmt/inventory/distribution/delDistribution"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
