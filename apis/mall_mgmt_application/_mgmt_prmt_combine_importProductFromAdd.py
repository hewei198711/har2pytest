import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_prmt_combine_importProductFromAdd(headers=headers):
    """
    导入商品解析
    /mgmt/prmt/combine/importProductFromAdd
    """

    url = "/mgmt/prmt/combine/importProductFromAdd"
    with client.post(url=url, headers=headers) as r:
        return r
