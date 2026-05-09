import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_sys_getLikeCountAndRecord(headers=headers):
    """
    查询当前店铺是否点赞及点赞总数
    /appStore/sys/getLikeCountAndRecord
    """

    url = "/appStore/sys/getLikeCountAndRecord"
    with client.get(url=url, headers=headers) as r:
        return r
