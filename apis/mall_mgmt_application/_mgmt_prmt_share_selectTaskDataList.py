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


def _mgmt_prmt_share_selectTaskDataList(params=params, headers=headers):
    """
    查询数据导出
    /mgmt/prmt/share/selectTaskDataList

    参数说明:
    - logDateMax: logDateMax
    - logDateMin: logDateMin
    - shareTaskId: shareTaskId
    """

    url = "/mgmt/prmt/share/selectTaskDataList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
