import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponTransfer_exportStoreTemplate(headers=headers):
    """
    下载导入门店模板
    /mgmt/prmt/couponTransfer/exportStoreTemplate
    """

    url = "/mgmt/prmt/couponTransfer/exportStoreTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
