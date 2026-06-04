import os

from util.client import client

params = {
    "productCode": "",  # productCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dis_inventory_split_forward(params=params, headers=headers):
    """
    拆分单个套装确认页
    /mgmt/dis-inventory/split/forward

    参数说明:
    - productCode: productCode
    """

    url = "/mgmt/dis-inventory/split/forward"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
