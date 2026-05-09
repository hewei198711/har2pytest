import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_dis_inventory_combine_detail(params=params, headers=headers):
    """
    套装组合明细
    /appStore/dis-inventory/combine/detail

    参数说明:
    - id: id
    """

    url = "/appStore/dis-inventory/combine/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
