import os

from util.client import client

params = {
    "regionCode": "",  # 区域编码
    "warehouseCode": "",  # 仓库编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getWareAndRegList(params=params, headers=headers):
    """
    仓库信息展示
    /mgmt/sys/getWareAndRegList

    参数说明:
    - regionCode: 区域编码
    - warehouseCode: 仓库编码
    """

    url = "/mgmt/sys/getWareAndRegList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
