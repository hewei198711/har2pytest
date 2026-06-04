import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_combine_exportProductTemplate(headers=headers):
    """
    商品导入模板下载
    /mgmt/prmt/combine/exportProductTemplate
    """

    url = "/mgmt/prmt/combine/exportProductTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
