import os

from util.client import client

params = {
    "depotId": 0,  # 仓库id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_depot_region_code_list(params=params, headers=headers):
    """
    根据仓库编码获取被绑定的地区编码集合
    /mgmt/sys/depot/region/code/list

    参数说明:
    - depotId: 仓库id
    """

    url = "/mgmt/sys/depot/region/code/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
