import os

from util.client import client

params = {
    "avatarId": 0,  # avatarId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_avatar_getAvatarInfo_avatarId(params=params, headers=headers):
    """
    获取头像图片信息
    /mgmt/cms/avatar/getAvatarInfo/{avatarId}

    参数说明:
    - avatarId: avatarId
    """

    url = f"/mgmt/cms/avatar/getAvatarInfo/{params['avatarId']}"
    with client.get(url=url, headers=headers) as r:
        return r
