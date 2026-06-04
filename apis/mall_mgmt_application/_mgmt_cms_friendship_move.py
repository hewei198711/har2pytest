import os

from util.client import client

data = {
    "id": 0,  # id
    "operate": 0,  # 排序操作，0：上移， 1：下移，2：置顶，3：置底
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_friendship_move(data=data, headers=headers):
    """
    友情链接排序，上移/下移/置顶/置底
    /mgmt/cms/friendship/move

    参数说明:
    - id: id
    - operate: 排序操作，0：上移， 1：下移，2：置顶，3：置底
    """

    url = "/mgmt/cms/friendship/move"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
