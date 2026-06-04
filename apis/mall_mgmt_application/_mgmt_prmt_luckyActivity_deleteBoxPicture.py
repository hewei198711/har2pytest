import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_deleteBoxPicture(params=params, headers=headers):
    """
    删除盲盒海报图片
    /mgmt/prmt/luckyActivity/deleteBoxPicture

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/luckyActivity/deleteBoxPicture"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
