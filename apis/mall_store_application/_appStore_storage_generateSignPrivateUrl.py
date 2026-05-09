import os

from util.client import client

data = {
    "urls": [],  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_storage_generateSignPrivateUrl(data=data, headers=headers):
    """
    生成签名url
    /appStore/storage/generateSignPrivateUrl
    """

    url = "/appStore/storage/generateSignPrivateUrl"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
