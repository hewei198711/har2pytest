import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_exportProductTemplate(headers=headers):
    """
    商品导入模板下载
    /mgmt/prmt/luckyActivity/exportProductTemplate
    """

    url = "/mgmt/prmt/luckyActivity/exportProductTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
