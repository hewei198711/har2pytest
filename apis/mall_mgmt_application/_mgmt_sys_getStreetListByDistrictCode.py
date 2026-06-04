import os

from util.client import client

params = {
    "districtCode": "",  # 地区编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getStreetListByDistrictCode(params=params, headers=headers):
    """
    根据城市编码获取下属地区
    /mgmt/sys/getStreetListByDistrictCode

    参数说明:
    - districtCode: 地区编码
    """

    url = "/mgmt/sys/getStreetListByDistrictCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
