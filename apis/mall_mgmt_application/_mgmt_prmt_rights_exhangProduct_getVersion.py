import os

from util.client import client

params = {
    "verId": "",  # verId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_rights_exhangProduct_getVersion(params=params, headers=headers):
    """
    查询兑换产品
    /mgmt/prmt/rights/exhangProduct/getVersion

    参数说明:
    - verId: verId
    """

    url = "/mgmt/prmt/rights/exhangProduct/getVersion"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
