import os

from util.client import client

params = {
    "key": "",  # key
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_downloadImportFailKeywords(params=params, headers=headers):
    """
    下载货到代收点关键词导入失败列表
    /mgmt/order/downloadImportFailKeywords

    参数说明:
    - key: key
    """

    url = "/mgmt/order/downloadImportFailKeywords"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
