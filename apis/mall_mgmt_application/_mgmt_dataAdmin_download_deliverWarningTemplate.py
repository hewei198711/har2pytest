import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_download_deliverWarningTemplate(headers=headers):
    """
    报单预警导入模板下载
    /mgmt/dataAdmin/download/deliverWarningTemplate
    """

    url = "/mgmt/dataAdmin/download/deliverWarningTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
