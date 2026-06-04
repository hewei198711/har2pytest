import os

from util.client import client

params = {
    "logDateMax": "",  # logDateMax
    "logDateMin": "",  # logDateMin
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
    "shareTaskId": 0,  # shareTaskId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_share_selectTaskDataPage(params=params, headers=headers):
    """
    分页查询数据
    /mgmt/prmt/share/selectTaskDataPage

    参数说明:
    - logDateMax: logDateMax
    - logDateMin: logDateMin
    - pageNum: pageNum
    - pageSize: pageSize
    - shareTaskId: shareTaskId
    """

    url = "/mgmt/prmt/share/selectTaskDataPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
