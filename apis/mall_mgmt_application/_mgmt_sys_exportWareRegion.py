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


def _mgmt_sys_exportWareRegion(params=params, headers=headers):
    """
    导出仓库信息
    /mgmt/sys/exportWareRegion

    参数说明:
    - regionCode: 区域编码
    - warehouseCode: 仓库编码
    """

    url = "/mgmt/sys/exportWareRegion"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
