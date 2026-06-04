import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_avatar_delAvatar(data=data, headers=headers):
    """
    删除头像图片
    /mgmt/cms/avatar/delAvatar

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/avatar/delAvatar"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
