import os

from util.client import client

params = {
    "provinceCode": "",  # 省份编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getCityList(params=params, headers=headers):
    """
    根据省份编码获取下属城市
    /mgmt/sys/getCityList

    参数说明:
    - provinceCode: 省份编码
    """

    url = "/mgmt/sys/getCityList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
