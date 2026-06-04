import os

from util.client import client

params = {
    "url": "",  # 上传到oss后返回的excel地址
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dis_inventory_split_reverse_batch_import(params=params, headers=headers):
    """
    保留套装批量上传
    /mgmt/dis-inventory/split/reverse/batch-import

    参数说明:
    - url: 上传到oss后返回的excel地址
    """

    url = "/mgmt/dis-inventory/split/reverse/batch-import"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
