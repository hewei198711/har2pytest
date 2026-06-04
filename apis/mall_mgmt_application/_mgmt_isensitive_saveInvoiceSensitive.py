import os

from util.client import client

data = {
    "invoiceSensitive": "",  # 敏感词
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_isensitive_saveInvoiceSensitive(data=data, headers=headers):
    """
    新增敏感词
    /mgmt/isensitive/saveInvoiceSensitive

    参数说明:
    - invoiceSensitive: 敏感词
    """

    url = "/mgmt/isensitive/saveInvoiceSensitive"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
