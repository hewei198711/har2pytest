import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_ecenter_getExperienceCenterProductById(params=params, headers=headers):
    """
    通过id获取体验中心商品信息
    /mgmt/ecenter/getExperienceCenterProductById

    参数说明:
    - id: id
    """

    url = "/mgmt/ecenter/getExperienceCenterProductById"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
