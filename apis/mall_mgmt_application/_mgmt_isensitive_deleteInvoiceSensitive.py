import os

from util.client import client

data = {
    "ids": [],  # 主键id集合
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_isensitive_deleteInvoiceSensitive(data=data, headers=headers):
    """
    删除敏感词
    /mgmt/isensitive/deleteInvoiceSensitive

    参数说明:
    - ids: 主键id集合
    """

    url = "/mgmt/isensitive/deleteInvoiceSensitive"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
