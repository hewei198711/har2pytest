import os

from util.client import client

params = {
    "splitId": 0,  # splitId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_bundle_batchExportFile(params=params, headers=headers):
    """
    调整明细导出--文件流
    /mgmt/product/bundle/batchExportFile

    参数说明:
    - splitId: splitId
    """

    url = "/mgmt/product/bundle/batchExportFile"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
