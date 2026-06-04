import os

from util.client import client

params = {
    "applianceRoleFlag": "",  # 适配对象
    "id": "",  # id主键
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_updateLogisticsOfRole(params=params, headers=headers):
    """
    编辑适用物流对象
    /mgmt/sys/updateLogisticsOfRole

    参数说明:
    - applianceRoleFlag: 适配对象
    - id: id主键
    """

    url = "/mgmt/sys/updateLogisticsOfRole"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
