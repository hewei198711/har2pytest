import os

from util.client import client

data = {
    "businessRange": 0,  # TODO: 添加参数说明
    "cityCode": "",  # 市编码
    "provinceCode": "",  # 省编码
    "sysDepotCode": "",  # 仓库编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_depot_district_batchUpdate(data=data, headers=headers):
    """
    批量修改区域对应仓库
    /mgmt/sys/depot/district/batchUpdate

    参数说明:
    - cityCode: 市编码
    - provinceCode: 省编码
    - sysDepotCode: 仓库编码
    """

    url = "/mgmt/sys/depot/district/batchUpdate"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
