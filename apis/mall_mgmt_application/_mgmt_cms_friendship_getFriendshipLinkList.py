import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_friendship_getFriendshipLinkList(headers=headers):
    """
    友情链接列表
    /mgmt/cms/friendship/getFriendshipLinkList
    """

    url = "/mgmt/cms/friendship/getFriendshipLinkList"
    with client.get(url=url, headers=headers) as r:
        return r
