import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_downloadDepositApplyTemplate(headers=headers):
    """
    批量保证金录入excel模板下载
    /mgmt/store/downloadDepositApplyTemplate
    """

    url = "/mgmt/store/downloadDepositApplyTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
