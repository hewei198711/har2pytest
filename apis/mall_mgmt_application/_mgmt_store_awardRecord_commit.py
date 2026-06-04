import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_awardRecord_commit(headers=headers):
    """
    批量导入图片(提交)
    /mgmt/store/awardRecord/commit
    """

    url = "/mgmt/store/awardRecord/commit"
    with client.post(url=url, headers=headers) as r:
        return r
