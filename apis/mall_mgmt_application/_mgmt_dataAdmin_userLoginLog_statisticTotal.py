import os

from util.client import client

params = {
    "dimension": 0,  # 统计维度 1：日 2：月
    "endTime": "",  # 结束时间,yyyy-MM-dd
    "startTime": "",  # 开始时间,yyyy-MM-dd
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_userLoginLog_statisticTotal(params=params, headers=headers):
    """
    用户登录统计总数
    /mgmt/dataAdmin/userLoginLog/statisticTotal

    参数说明:
    - dimension: 统计维度 1：日 2：月
    - endTime: 结束时间,yyyy-MM-dd
    - startTime: 开始时间,yyyy-MM-dd
    """

    url = "/mgmt/dataAdmin/userLoginLog/statisticTotal"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
