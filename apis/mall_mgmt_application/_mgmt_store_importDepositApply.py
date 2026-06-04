import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_importDepositApply(headers=headers):
    """
    批量导入保证金申请
    /mgmt/store/importDepositApply
    """

    url = "/mgmt/store/importDepositApply"
    with client.post(url=url, headers=headers) as r:
        return r
