import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_productReportApply_exportFailList(headers=headers):
    """
    成品报告审批导出失败记录
    /mgmt/store/productReportApply/exportFailList
    """

    url = "/mgmt/store/productReportApply/exportFailList"
    with client.get(url=url, headers=headers) as r:
        return r
