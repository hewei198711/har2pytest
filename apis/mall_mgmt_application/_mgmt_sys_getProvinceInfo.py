import os

from util.client import client

params = {
    "id": "",  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getProvinceInfo(params=params, headers=headers):
    """
    新增时此仓库被选的省份和其他仓库被选的省份
    /mgmt/sys/getProvinceInfo

    参数说明:
    - id: id
    """

    url = "/mgmt/sys/getProvinceInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
