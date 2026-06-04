import os

from util.client import client

params = {
    "reserveId": 0,  # reserveId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_bundle_getReserveBundleInfo(params=params, headers=headers):
    """
    查询套装信息
    /mgmt/product/bundle/getReserveBundleInfo

    参数说明:
    - reserveId: reserveId
    """

    url = "/mgmt/product/bundle/getReserveBundleInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
