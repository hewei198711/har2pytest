import os

from util.client import client

params = {
    "endTime": "",  # endTime
    "startTime": "",  # startTime
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_skin_list(params=params, headers=headers):
    """
    精准护肤统计数据列表
    /mgmt/skin/list

    参数说明:
    - endTime: endTime
    - startTime: startTime
    """

    url = "/mgmt/skin/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
