import os

from util.client import client

data = {
    "businessRange": 0,  # 业务范围:1->B,2->C,3->B+C
    "id": 0,  # 主键id
    "stcType": 0,  # 交通管理类型,1:立即生效; 2:定时生效;3:定时生效和失效 4:立即失效
    "stcwId": 0,  # 交通管制提示语id
    "timeOff": 0,  # 定时失效时间
    "timeUp": 0,  # 定时生效时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_traffic_updateTrafficControl(data=data, headers=headers):
    """
    更新交通管制
    /mgmt/sys/traffic/updateTrafficControl

    参数说明:
    - businessRange: 业务范围:1->B,2->C,3->B+C
    - id: 主键id
    - stcType: 交通管理类型,1:立即生效; 2:定时生效;3:定时生效和失效 4:立即失效
    - stcwId: 交通管制提示语id
    - timeOff: 定时失效时间
    - timeUp: 定时生效时间
    """

    url = "/mgmt/sys/traffic/updateTrafficControl"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
