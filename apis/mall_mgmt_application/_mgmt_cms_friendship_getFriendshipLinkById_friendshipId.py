import os

from util.client import client

params = {
    "friendshipId": 0,  # friendshipId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_friendship_getFriendshipLinkById_friendshipId(params=params, headers=headers):
    """
    获取友情链接
    /mgmt/cms/friendship/getFriendshipLinkById/{friendshipId}

    参数说明:
    - friendshipId: friendshipId
    """

    url = f"/mgmt/cms/friendship/getFriendshipLinkById/{params['friendshipId']}"
    with client.get(url=url, headers=headers) as r:
        return r
