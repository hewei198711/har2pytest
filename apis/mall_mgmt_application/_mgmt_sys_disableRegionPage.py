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


def _mgmt_sys_disableRegionPage(params=params, headers=headers):
    """
    分页查询隐藏地区列表
    /mgmt/sys/disableRegionPage

    参数说明:
    - pageNum: pageNum
    - pageSize: pageSize
    """

    url = "/mgmt/sys/disableRegionPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
