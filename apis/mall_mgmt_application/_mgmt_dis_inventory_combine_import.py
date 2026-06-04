import os

from util.client import client

params = {
    "url": "",  # 上传到oss后返回的excel地址
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dis_inventory_combine_import(params=params, headers=headers):
    """
    导入批量组合
    /mgmt/dis-inventory/combine/import

    参数说明:
    - url: 上传到oss后返回的excel地址
    """

    url = "/mgmt/dis-inventory/combine/import"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
