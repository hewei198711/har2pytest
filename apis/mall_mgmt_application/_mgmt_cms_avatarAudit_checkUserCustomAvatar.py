import os

from util.client import client

params = {
    "userId": 0,  # userId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_avatarAudit_checkUserCustomAvatar(params=params, headers=headers):
    """
    检查用户自定义头像相关信息
    /mgmt/cms/avatarAudit/checkUserCustomAvatar

    参数说明:
    - userId: userId
    """

    url = "/mgmt/cms/avatarAudit/checkUserCustomAvatar"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
