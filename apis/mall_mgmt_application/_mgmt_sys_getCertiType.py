import os

from util.client import client

params = {
    "pageNum": 0,  # 页码不能少于1,默认1
    "pageSize": 0,  # 显示条数不能少于1,默认10
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getCertiType(params=params, headers=headers):
    """
    分页展示证件类型
    /mgmt/sys/getCertiType

    参数说明:
    - pageNum: 页码不能少于1,默认1
    - pageSize: 显示条数不能少于1,默认10
    """

    url = "/mgmt/sys/getCertiType"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
