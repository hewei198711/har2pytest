import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_prmt_libertySale_importProductFromAdd(headers=headers):
    """
    活动新增页面-导入商品
    /mgmt/prmt/libertySale/importProductFromAdd
    """

    url = "/mgmt/prmt/libertySale/importProductFromAdd"
    with client.post(url=url, headers=headers) as r:
        return r
