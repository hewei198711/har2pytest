import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_prmt_combine_editGiftSort(headers=headers):
    """
    详情页赠品池商品调整排序
    /mgmt/prmt/combine/editGiftSort
    """

    url = "/mgmt/prmt/combine/editGiftSort"
    with client.post(url=url, headers=headers) as r:
        return r
