import os

from util.client import client

data = {
    "city": "",  # 城市
    "levelName": "",  # 城市等级
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "province": "",  # 省份
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_city_level_page(data=data, headers=headers):
    """
    分页查询城市等级列表
    /mgmt/sys/city-level/page

    参数说明:
    - city: 城市
    - levelName: 城市等级
    - province: 省份
    """

    url = "/mgmt/sys/city-level/page"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
