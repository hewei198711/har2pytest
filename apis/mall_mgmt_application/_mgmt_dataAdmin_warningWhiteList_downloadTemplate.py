import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_dataAdmin_warningWhiteList_downloadTemplate(headers=headers):
    """
    下载-导入预警白名单模版
    /mgmt/dataAdmin/warningWhiteList/downloadTemplate
    """

    url = "/mgmt/dataAdmin/warningWhiteList/downloadTemplate"
    with client.post(url=url, headers=headers) as r:
        return r
