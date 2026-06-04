import os

from util.client import client

params = {
    "businessRange": 0,  # 业务范围
    "depotCode": "",  # 仓库编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_depot_list(params=params, headers=headers):
    """
    获取仓库信息集合
    /mgmt/sys/depot/list

    参数说明:
    - businessRange: 业务范围
    - depotCode: 仓库编码
    """

    url = "/mgmt/sys/depot/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
