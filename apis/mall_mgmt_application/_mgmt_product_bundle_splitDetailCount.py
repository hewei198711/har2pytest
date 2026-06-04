import os

from util.client import client

params = {
    "splitId": "",  # 拆分id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_bundle_splitDetailCount(params=params, headers=headers):
    """
    拆分明细数量统计--拆分后
    /mgmt/product/bundle/splitDetailCount

    参数说明:
    - splitId: 拆分id
    """

    url = "/mgmt/product/bundle/splitDetailCount"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
