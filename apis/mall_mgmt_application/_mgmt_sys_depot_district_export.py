import os

from util.client import client

data = {
    "businessRange": 0,  # 业务范围: 1.B 2.C 3.B+C 4.赠品区域
    "cityCode": "",  # 市编码
    "districtCode": "",  # 区县编码
    "provinceCode": "",  # 省编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_depot_district_export(data=data, headers=headers):
    """
    导出区域仓库信息
    /mgmt/sys/depot/district/export

    参数说明:
    - businessRange: 业务范围: 1.B 2.C 3.B+C 4.赠品区域
    - cityCode: 市编码
    - districtCode: 区县编码
    - provinceCode: 省编码
    """

    url = "/mgmt/sys/depot/district/export"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
