import os

from util.client import client

params = {
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 页面大小
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_report_PageReportQueryRanges(params=params, headers=headers):
    """
    分页查询报表表查询范围
    /mgmt/sys/report/PageReportQueryRanges

    参数说明:
    - pageNum: 页码
    - pageSize: 页面大小
    """

    url = "/mgmt/sys/report/PageReportQueryRanges"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
