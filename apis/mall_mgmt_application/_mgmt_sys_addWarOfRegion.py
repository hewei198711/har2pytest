import os

from util.client import client

data = {
    "regionCodes": [],  # 区域编码集
    "warehouseId": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_addWarOfRegion(data=data, headers=headers):
    """
    新增仓库省份信息
    /mgmt/sys/addWarOfRegion

    参数说明:
    - regionCodes: 区域编码集
    - warehouseId: id
    """

    url = "/mgmt/sys/addWarOfRegion"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
