import os

from util.client import client

data = {
    "combines": [{"combineNum": 0, "productCode": "", "storeCode": ""}],  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dis_inventory_combine_batch(data=data, headers=headers):
    """
    批量套装组合
    /mgmt/dis-inventory/combine/batch
    """

    url = "/mgmt/dis-inventory/combine/batch"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
