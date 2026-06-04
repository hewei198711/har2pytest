import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_getBoxRemarkInfo(params=params, headers=headers):
    """
    获取盲盒海报文案详情
    /mgmt/prmt/luckyActivity/getBoxRemarkInfo

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/luckyActivity/getBoxRemarkInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
