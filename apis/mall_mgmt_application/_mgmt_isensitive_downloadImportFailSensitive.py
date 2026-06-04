import os

from util.client import client

params = {
    "key": "",  # key
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_isensitive_downloadImportFailSensitive(params=params, headers=headers):
    """
    下载敏感词导入失败列表
    /mgmt/isensitive/downloadImportFailSensitive

    参数说明:
    - key: key
    """

    url = "/mgmt/isensitive/downloadImportFailSensitive"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
