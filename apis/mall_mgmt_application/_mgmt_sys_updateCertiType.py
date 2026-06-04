import os

from util.client import client

data = {
    "id": 0,  # id
    "remarks": "",  # 备注
    "typeName": "",  # 类型名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_updateCertiType(data=data, headers=headers):
    """
    编辑证件类型
    /mgmt/sys/updateCertiType

    参数说明:
    - id: id
    - remarks: 备注
    - typeName: 类型名称
    """

    url = "/mgmt/sys/updateCertiType"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
