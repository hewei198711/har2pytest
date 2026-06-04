import os

from util.client import client

data = {
    "id": 0,  # 仓库区域id
    "sysDepotCode": "",  # 仓库编码
    "sysDepotStatus": 0,  # 状态 1：生效 -1：失效
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_depot_district_update(data=data, headers=headers):
    """
    修改区域对应仓库
    /mgmt/sys/depot/district/update

    参数说明:
    - id: 仓库区域id
    - sysDepotCode: 仓库编码
    - sysDepotStatus: 状态 1：生效 -1：失效
    """

    url = "/mgmt/sys/depot/district/update"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
