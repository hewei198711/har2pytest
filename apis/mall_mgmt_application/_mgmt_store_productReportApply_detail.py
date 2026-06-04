import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_productReportApply_detail(params=params, headers=headers):
    """
    运营后台:根据id获取详情
    /mgmt/store/productReportApply/detail

    参数说明:
    - id: id
    """

    url = "/mgmt/store/productReportApply/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
