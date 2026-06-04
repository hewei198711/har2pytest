import os

from util.client import client

params = {
    "friendshipId": 0,  # friendshipId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_friendship_removeFriendshipLink_friendshipId(params=params, headers=headers):
    """
    删除友情链接
    /mgmt/cms/friendship/removeFriendshipLink/{friendshipId}

    参数说明:
    - friendshipId: friendshipId
    """

    url = f"/mgmt/cms/friendship/removeFriendshipLink/{params['friendshipId']}"
    with client.get(url=url, headers=headers) as r:
        return r
