import os

from util.client import client

params = {
    "businessRange": 0,  # 业务范围
    "depotId": 0,  # 仓库id
    "provinceCodes": [],  # 省份编码集合
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_depot_region_list(params=params, headers=headers):
    """
    查询仓库绑定的地区信息列表
    /mgmt/sys/depot/region/list

    参数说明:
    - businessRange: 业务范围
    - depotId: 仓库id
    - provinceCodes: 省份编码集合
    """

    url = "/mgmt/sys/depot/region/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
