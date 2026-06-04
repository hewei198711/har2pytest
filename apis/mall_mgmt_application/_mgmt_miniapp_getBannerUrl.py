import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_miniapp_getBannerUrl(headers=headers):
    """
    获取直播banner图片
    /mgmt/miniapp/getBannerUrl
    """

    url = "/mgmt/miniapp/getBannerUrl"
    with client.get(url=url, headers=headers) as r:
        return r
