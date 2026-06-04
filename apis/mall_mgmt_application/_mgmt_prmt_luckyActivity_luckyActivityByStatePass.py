import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_luckyActivityByStatePass(headers=headers):
    """
    查询待开始,进行中抽奖活动.
    /mgmt/prmt/luckyActivity/luckyActivityByStatePass
    """

    url = "/mgmt/prmt/luckyActivity/luckyActivityByStatePass"
    with client.get(url=url, headers=headers) as r:
        return r
