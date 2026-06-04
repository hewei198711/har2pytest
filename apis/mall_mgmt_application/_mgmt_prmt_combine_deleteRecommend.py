import os

from util.client import client

params = {
    "recommendId": 0,  # recommendId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_combine_deleteRecommend(params=params, headers=headers):
    """
    根据推荐组合id删除推荐组合
    /mgmt/prmt/combine/deleteRecommend

    参数说明:
    - recommendId: recommendId
    """

    url = "/mgmt/prmt/combine/deleteRecommend"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
