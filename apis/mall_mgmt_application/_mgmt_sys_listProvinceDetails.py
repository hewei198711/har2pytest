import os

from util.client import client

params = {
    "provinceCodes": "",  # 省份编码集合
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_listProvinceDetails(params=params, headers=headers):
    """
    根据省份编码集合获取省份信息及下属地区信息
    /mgmt/sys/listProvinceDetails

    参数说明:
    - provinceCodes: 省份编码集合
    """

    url = "/mgmt/sys/listProvinceDetails"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
