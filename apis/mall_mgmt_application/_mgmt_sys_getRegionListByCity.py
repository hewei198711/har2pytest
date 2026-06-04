import os

from util.client import client

params = {
    "cityCode": "",  # 城市编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getRegionListByCity(params=params, headers=headers):
    """
    根据城市编码获取下属地区
    /mgmt/sys/getRegionListByCity

    参数说明:
    - cityCode: 城市编码
    """

    url = "/mgmt/sys/getRegionListByCity"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
