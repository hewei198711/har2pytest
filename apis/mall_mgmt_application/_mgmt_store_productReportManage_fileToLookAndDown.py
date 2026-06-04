import os

from util.client import client

params = {
    "id": 0,  # id
    "no": 0,  # no
    "type": 0,  # type
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_productReportManage_fileToLookAndDown(params=params, headers=headers):
    """
    预览或者下载成品报告:1预览 2下载
    /mgmt/store/productReportManage/fileToLookAndDown

    参数说明:
    - id: id
    - no: no
    - type: type
    """

    url = "/mgmt/store/productReportManage/fileToLookAndDown"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
