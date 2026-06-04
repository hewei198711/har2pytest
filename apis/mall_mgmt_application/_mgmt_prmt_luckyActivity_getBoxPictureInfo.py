import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_getBoxPictureInfo(params=params, headers=headers):
    """
    获取盲盒海报图片详情
    /mgmt/prmt/luckyActivity/getBoxPictureInfo

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/luckyActivity/getBoxPictureInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
