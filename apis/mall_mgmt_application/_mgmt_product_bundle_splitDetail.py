import os

from util.client import client

params = {
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
    "splitId": "",  # 拆分id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_bundle_splitDetail(params=params, headers=headers):
    """
    拆分明细
    /mgmt/product/bundle/splitDetail

    参数说明:
    - pageNum: pageNum
    - pageSize: pageSize
    - splitId: 拆分id
    """

    url = "/mgmt/product/bundle/splitDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
