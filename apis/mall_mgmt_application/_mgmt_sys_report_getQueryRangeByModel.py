import os

from util.client import client

params = {
    "reportModel": 0,  # 模块
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_report_getQueryRangeByModel(params=params, headers=headers):
    """
    根据模块来获取最新的查询范围
    /mgmt/sys/report/getQueryRangeByModel

    参数说明:
    - reportModel: 模块
    """

    url = "/mgmt/sys/report/getQueryRangeByModel"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
