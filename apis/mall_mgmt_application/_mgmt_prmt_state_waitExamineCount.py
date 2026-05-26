import os

from util.client import client

headers = {
    "channel": "pc",
    "client": "op",
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_prmt_state_waitExamineCount(headers=headers):
    """
    待审核状态数量
    /mgmt/prmt/state/waitExamineCount
    """

    url = "/mgmt/prmt/state/waitExamineCount"
    with client.get(url=url, headers=headers) as r:
        return r
