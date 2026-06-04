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


def _mgmt_sys_addCertiType(data=data, headers=headers):
    """
    证件类型新增
    /mgmt/sys/addCertiType

    参数说明:
    - id: id
    - remarks: 备注
    - typeName: 类型名称
    """

    url = "/mgmt/sys/addCertiType"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
