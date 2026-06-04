import os

from util.client import client

params = {
    "key": "",  # key
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_downloadImportFailProduct(params=params, headers=headers):
    """
    下载商品导入失败列表
    /mgmt/prmt/luckyActivity/downloadImportFailProduct

    参数说明:
    - key: key
    """

    url = "/mgmt/prmt/luckyActivity/downloadImportFailProduct"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
