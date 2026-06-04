import os

from util.client import client

data = {
    "changeReason": "",  # 变更原因
    "city": "",  # 城市
    "id": 0,  # ID
    "levelName": "",  # 城市等级
    "operator": "",  # 操作人
    "operatorId": "",  # 操作人工号
    "province": "",  # 省份
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_city_level_add(data=data, headers=headers):
    """
    新增城市等级
    /mgmt/sys/city-level/add

    参数说明:
    - changeReason: 变更原因
    - city: 城市
    - id: ID
    - levelName: 城市等级
    - operator: 操作人
    - operatorId: 操作人工号
    - province: 省份
    """

    url = "/mgmt/sys/city-level/add"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
