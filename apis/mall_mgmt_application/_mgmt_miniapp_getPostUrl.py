import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_miniapp_getPostUrl(headers=headers):
    """
    获取直播分享海报信息
    /mgmt/miniapp/getPostUrl
    """

    url = "/mgmt/miniapp/getPostUrl"
    with client.get(url=url, headers=headers) as r:
        return r
