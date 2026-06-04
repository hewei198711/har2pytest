import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_share_getTaskById(params=params, headers=headers):
    """
    根据id查询分享领券活动（用于编辑回显）
    /mgmt/prmt/share/getTaskById

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/share/getTaskById"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
