import os

from util.client import client

params = {
    "businessRange": 0,  # businessRange
    "depotId": 0,  # 仓库id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_depot_province_list(params=params, headers=headers):
    """
    查询仓库绑定的省份列表
    /mgmt/sys/depot/province/list

    参数说明:
    - businessRange: businessRange
    - depotId: 仓库id
    """

    url = "/mgmt/sys/depot/province/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
