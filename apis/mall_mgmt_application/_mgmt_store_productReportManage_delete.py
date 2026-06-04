import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_productReportManage_delete(params=params, headers=headers):
    """
    删除成品报告
    /mgmt/store/productReportManage/delete

    参数说明:
    - id: id
    """

    url = "/mgmt/store/productReportManage/delete"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
