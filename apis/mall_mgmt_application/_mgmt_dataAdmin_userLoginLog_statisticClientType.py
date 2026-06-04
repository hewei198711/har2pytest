import os

from util.client import client

params = {
    "endTime": "",  # 结束时间,yyyy-MM-dd
    "startTime": "",  # 开始时间,yyyy-MM-dd
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_userLoginLog_statisticClientType(params=params, headers=headers):
    """
    用户登录端统计
    /mgmt/dataAdmin/userLoginLog/statisticClientType

    参数说明:
    - endTime: 结束时间,yyyy-MM-dd
    - startTime: 开始时间,yyyy-MM-dd
    """

    url = "/mgmt/dataAdmin/userLoginLog/statisticClientType"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
