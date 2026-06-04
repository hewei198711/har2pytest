import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_avatarFrame_delAvatarFrame(data=data, headers=headers):
    """
    删除头像框图片
    /mgmt/cms/avatarFrame/delAvatarFrame

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/avatarFrame/delAvatarFrame"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
