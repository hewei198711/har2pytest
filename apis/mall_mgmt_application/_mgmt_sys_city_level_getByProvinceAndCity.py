import os

from util.client import client

params = {
    "city": "",  # city
    "province": "",  # province
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_city_level_getByProvinceAndCity(params=params, headers=headers):
    """
    根据省份和城市查询城市等级
    /mgmt/sys/city-level/getByProvinceAndCity

    参数说明:
    - city: city
    - province: province
    """

    url = "/mgmt/sys/city-level/getByProvinceAndCity"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
