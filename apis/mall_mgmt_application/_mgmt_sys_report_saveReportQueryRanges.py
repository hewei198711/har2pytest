import os

from util.client import client

data = {
    "queryRange": 0,  # 查询范围
    "reportModel": 0,  # 模块：1-享受服务费的订单汇总；2-各系列产品业绩统计表
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_report_saveReportQueryRanges(data=data, headers=headers):
    """
    配置查询范围
    /mgmt/sys/report/saveReportQueryRanges

    参数说明:
    - queryRange: 查询范围
    - reportModel: 模块：1-享受服务费的订单汇总；2-各系列产品业绩统计表
    """

    url = "/mgmt/sys/report/saveReportQueryRanges"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
