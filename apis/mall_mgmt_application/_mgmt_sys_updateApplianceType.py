import os

from util.client import client

data = {
    "applianceRoleFlag": [],  # 类型
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_updateApplianceType(data=data, headers=headers):
    """
    编辑支付适用对象
    /mgmt/sys/updateApplianceType

    参数说明:
    - applianceRoleFlag: 类型
    - id: id
    """

    url = "/mgmt/sys/updateApplianceType"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
