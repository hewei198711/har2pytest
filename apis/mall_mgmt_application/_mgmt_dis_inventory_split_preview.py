import os

from util.client import client

data = {
    "productCodes": [],  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dis_inventory_split_preview(data=data, headers=headers):
    """
    套装拆分预览
    /mgmt/dis-inventory/split/preview
    """

    url = "/mgmt/dis-inventory/split/preview"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
