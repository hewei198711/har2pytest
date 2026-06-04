import os

from util.client import client

params = {
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_city_level_change_log_page(params=params, headers=headers):
    """
    分页查询城市等级变更记录
    /mgmt/sys/city-level/change-log/page

    参数说明:
    - pageNum: pageNum
    - pageSize: pageSize
    """

    url = "/mgmt/sys/city-level/change-log/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
