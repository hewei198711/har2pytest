import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_state_waitExamineCount(headers=headers):
    """
    待审核状态数量
    /mgmt/prmt/state/waitExamineCount
    """

    url = "/mgmt/prmt/state/waitExamineCount"
    with client.get(url=url, headers=headers) as r:
        return r
