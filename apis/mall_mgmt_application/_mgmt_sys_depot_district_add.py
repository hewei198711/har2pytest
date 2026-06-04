import os

from util.client import client

data = {
    "cityCode": "",  # 市编码
    "cityName": "",  # 市
    "districtCode": "",  # 区县编码
    "districtName": "",  # 区县
    "provinceCode": "",  # 省编码
    "provinceName": "",  # 省
    "sysDepotCode": "",  # 仓库编码
    "sysDepotStatus": 0,  # 状态 1：生效 -1：失效
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_depot_district_add(data=data, headers=headers):
    """
    添加区域仓库
    /mgmt/sys/depot/district/add

    参数说明:
    - cityCode: 市编码
    - cityName: 市
    - districtCode: 区县编码
    - districtName: 区县
    - provinceCode: 省编码
    - provinceName: 省
    - sysDepotCode: 仓库编码
    - sysDepotStatus: 状态 1：生效 -1：失效
    """

    url = "/mgmt/sys/depot/district/add"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
