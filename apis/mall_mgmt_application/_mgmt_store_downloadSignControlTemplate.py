import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_downloadSignControlTemplate(headers=headers):
    """
    下载服务中心签署控制导入模板
    /mgmt/store/downloadSignControlTemplate
    """

    url = "/mgmt/store/downloadSignControlTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
