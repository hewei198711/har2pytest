import os

from util.client import client

params = {
    "friendshipId": 0,  # friendshipId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_friendship_editFriendshipLink_friendshipId(params=params, headers=headers):
    """
    编辑友情链接
    /mgmt/cms/friendship/editFriendshipLink/{friendshipId}

    参数说明:
    - friendshipId: friendshipId
    - linkName: 友情链接名称
    - linkUrl: 友情链接地址
    - parentId: 父ID
    """

    url = f"/mgmt/cms/friendship/editFriendshipLink/{params['friendshipId']}"
    with client.get(url=url, headers=headers) as r:
        return r
