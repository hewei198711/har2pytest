import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_exportPerformanceAppraisalFailList(headers=headers):
    """
    导出服务中心业绩目标失败列表
    /mgmt/store/exportPerformanceAppraisalFailList
    """

    url = "/mgmt/store/exportPerformanceAppraisalFailList"
    with client.get(url=url, headers=headers) as r:
        return r
