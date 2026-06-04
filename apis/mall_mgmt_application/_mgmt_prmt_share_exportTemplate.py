import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_share_exportTemplate(headers=headers):
    """
    下载导入可参与分享领券活动顾客模板
    /mgmt/prmt/share/exportTemplate
    """

    url = "/mgmt/prmt/share/exportTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
