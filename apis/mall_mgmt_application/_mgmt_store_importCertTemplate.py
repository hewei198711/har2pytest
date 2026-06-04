import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_importCertTemplate(headers=headers):
    """
    电子印章认证信息导入模板
    /mgmt/store/importCertTemplate
    """

    url = "/mgmt/store/importCertTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
