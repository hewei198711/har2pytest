import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_download_shopWarningTemplate(headers=headers):
    """
    重点购货预警名单导入模板下载
    /mgmt/dataAdmin/download/shopWarningTemplate
    """

    url = "/mgmt/dataAdmin/download/shopWarningTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
