import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_shelvesCoupon_exportTemplate(headers=headers):
    """
    下载导入上架对象模板
    /mgmt/prmt/shelvesCoupon/exportTemplate
    """

    url = "/mgmt/prmt/shelvesCoupon/exportTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
