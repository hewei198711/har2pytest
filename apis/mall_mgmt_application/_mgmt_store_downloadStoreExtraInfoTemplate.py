import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_downloadStoreExtraInfoTemplate(headers=headers):
    """
    下载服务中心层级调整模板
    /mgmt/store/downloadStoreExtraInfoTemplate
    """

    url = "/mgmt/store/downloadStoreExtraInfoTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
