import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_productReportApply_excelBatchImport(headers=headers):
    """
    成品报告审批Excel批量导入
    /mgmt/store/productReportApply/excelBatchImport
    """

    url = "/mgmt/store/productReportApply/excelBatchImport"
    with client.post(url=url, headers=headers) as r:
        return r
