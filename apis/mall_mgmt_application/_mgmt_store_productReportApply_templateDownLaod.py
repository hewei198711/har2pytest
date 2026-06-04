import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_productReportApply_templateDownLaod(headers=headers):
    """
    成品报告审批批量导入模板下载
    /mgmt/store/productReportApply/templateDownLaod
    """

    url = "/mgmt/store/productReportApply/templateDownLaod"
    with client.get(url=url, headers=headers) as r:
        return r
