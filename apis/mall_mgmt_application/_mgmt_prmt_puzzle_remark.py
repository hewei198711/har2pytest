import os

from util.client import client

data = {
    "id": 0,  # 活动id
    "remark": "",  # 活动规则(富文本)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_puzzle_remark(data=data, headers=headers):
    """
    修改活动规则富文本
    /mgmt/prmt/puzzle/remark

    参数说明:
    - id: 活动id
    - remark: 活动规则(富文本)
    """

    url = "/mgmt/prmt/puzzle/remark"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
