import os

from util.client import client

params = {
    "serialNo": "",  # serialNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_shoppedGift_searchProduct(params=params, headers=headers):
    """
    搜索产品
    /mgmt/prmt/shoppedGift/searchProduct

    参数说明:
    - serialNo: serialNo
    """

    url = "/mgmt/prmt/shoppedGift/searchProduct"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
