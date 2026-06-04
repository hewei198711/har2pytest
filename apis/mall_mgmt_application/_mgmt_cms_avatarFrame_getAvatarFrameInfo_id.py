import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_avatarFrame_getAvatarFrameInfo_id(params=params, headers=headers):
    """
    获取头像框图片信息
    /mgmt/cms/avatarFrame/getAvatarFrameInfo/{id}

    参数说明:
    - id: id
    """

    url = f"/mgmt/cms/avatarFrame/getAvatarFrameInfo/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
