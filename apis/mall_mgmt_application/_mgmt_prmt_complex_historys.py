import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_complex_historys(params=params, headers=headers):
    """
    获取历史版本列表
    /mgmt/prmt/complex/historys

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/complex/historys"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
