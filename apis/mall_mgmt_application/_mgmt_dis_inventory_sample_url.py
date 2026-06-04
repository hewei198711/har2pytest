import os

from util.client import client

params = {
    "key": "",  # key
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dis_inventory_sample_url(params=params, headers=headers):
    """
    获取85折库存模板路径
    /mgmt/dis-inventory/sample-url

    参数说明:
    - key: key
    """

    url = "/mgmt/dis-inventory/sample-url"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
