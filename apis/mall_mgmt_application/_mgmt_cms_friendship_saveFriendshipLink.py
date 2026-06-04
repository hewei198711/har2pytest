import os

from util.client import client

data = {
    "linkName": "",  # 友情链接名称
    "linkUrl": "",  # 友情链接地址
    "parentId": 0,  # 父ID
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_friendship_saveFriendshipLink(data=data, headers=headers):
    """
    新增友情链接
    /mgmt/cms/friendship/saveFriendshipLink

    参数说明:
    - linkName: 友情链接名称
    - linkUrl: 友情链接地址
    - parentId: 父ID
    """

    url = "/mgmt/cms/friendship/saveFriendshipLink"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
