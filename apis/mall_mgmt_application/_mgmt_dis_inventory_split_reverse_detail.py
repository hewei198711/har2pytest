import os

from util.client import client

params = {
    "reserveId": 0,  # reserveId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dis_inventory_split_reverse_detail(params=params, headers=headers):
    """
    查询套装信息
    /mgmt/dis-inventory/split/reverse/detail

    参数说明:
    - reserveId: reserveId
    """

    url = "/mgmt/dis-inventory/split/reverse/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
