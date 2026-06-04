import os

from util.client import client

params = {
    "logDateMax": "",  # logDateMax
    "logDateMin": "",  # logDateMin
    "shareTaskId": 0,  # shareTaskId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_share_selectTaskData(params=params, headers=headers):
    """
    查询数据汇总
    /mgmt/prmt/share/selectTaskData

    参数说明:
    - logDateMax: logDateMax
    - logDateMin: logDateMin
    - shareTaskId: shareTaskId
    """

    url = "/mgmt/prmt/share/selectTaskData"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
