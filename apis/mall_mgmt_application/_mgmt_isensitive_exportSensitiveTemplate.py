import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_isensitive_exportSensitiveTemplate(headers=headers):
    """
    导入模板下载
    /mgmt/isensitive/exportSensitiveTemplate
    """

    url = "/mgmt/isensitive/exportSensitiveTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
