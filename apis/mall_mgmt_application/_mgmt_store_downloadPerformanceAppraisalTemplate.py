import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_downloadPerformanceAppraisalTemplate(headers=headers):
    """
    下载服务中心业绩目标导入模板
    /mgmt/store/downloadPerformanceAppraisalTemplate
    """

    url = "/mgmt/store/downloadPerformanceAppraisalTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
