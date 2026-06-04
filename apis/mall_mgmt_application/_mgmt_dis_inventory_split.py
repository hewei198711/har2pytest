import os

from util.client import client

data = {
    "productCodes": [],  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dis_inventory_split(data=data, headers=headers):
    """
    套装拆分
    /mgmt/dis-inventory/split
    """

    url = "/mgmt/dis-inventory/split"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
