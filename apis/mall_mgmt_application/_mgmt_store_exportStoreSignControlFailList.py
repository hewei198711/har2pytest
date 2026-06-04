import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_exportStoreSignControlFailList(headers=headers):
    """
    导出服务中心签署控制失败列表
    /mgmt/store/exportStoreSignControlFailList
    """

    url = "/mgmt/store/exportStoreSignControlFailList"
    with client.get(url=url, headers=headers) as r:
        return r
