import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_getPromotionById(params=params, headers=headers):
    """
    根据id查询活动（用于编辑回显）
    /mgmt/prmt/getPromotionById

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/getPromotionById"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
