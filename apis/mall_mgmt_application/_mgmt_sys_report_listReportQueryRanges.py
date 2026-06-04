import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_report_listReportQueryRanges(headers=headers):
    """
    获取报表查询范围列表
    /mgmt/sys/report/listReportQueryRanges
    """

    url = "/mgmt/sys/report/listReportQueryRanges"
    with client.get(url=url, headers=headers) as r:
        return r
