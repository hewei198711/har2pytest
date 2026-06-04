import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_prmt_combine_addGift(headers=headers):
    """
    详情页添加赠品池商品
    /mgmt/prmt/combine/addGift
    """

    url = "/mgmt/prmt/combine/addGift"
    with client.post(url=url, headers=headers) as r:
        return r
