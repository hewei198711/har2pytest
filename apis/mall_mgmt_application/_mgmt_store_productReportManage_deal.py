import os

from util.client import client

params = {
    "id": 0,  # id
    "status": 0,  # status
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_productReportManage_deal(params=params, headers=headers):
    """
    修改报告状态 0禁用 1启用
    /mgmt/store/productReportManage/deal

    参数说明:
    - id: id
    - status: status
    """

    url = "/mgmt/store/productReportManage/deal"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
