import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_authorization_getLatestSetDownloadTimesLog(headers=headers):
    """
    获取最新一条设置下载次数的操作记录
    /mgmt/store/authorization/getLatestSetDownloadTimesLog
    """

    url = "/mgmt/store/authorization/getLatestSetDownloadTimesLog"
    with client.get(url=url, headers=headers) as r:
        return r
