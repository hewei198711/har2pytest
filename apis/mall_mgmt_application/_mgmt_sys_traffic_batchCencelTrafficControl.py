import os

from util.client import client

data = {
    "ids": [],  # 主键id集合
    "stcType": 0,  # 交通管理 类型4:立即失效
    "stcwId": 0,  # 交通管制提示语id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_traffic_batchCencelTrafficControl(data=data, headers=headers):
    """
    批量取消交通管制
    /mgmt/sys/traffic/batchCencelTrafficControl

    参数说明:
    - ids: 主键id集合
    - stcType: 交通管理 类型4:立即失效
    - stcwId: 交通管制提示语id
    """

    url = "/mgmt/sys/traffic/batchCencelTrafficControl"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
