import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_selectPerformanceAppraisalById(params=params, headers=headers):
    """
    根据ID查询服务中心业绩目标
    /mgmt/store/selectPerformanceAppraisalById

    参数说明:
    - id: id
    """

    url = "/mgmt/store/selectPerformanceAppraisalById"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
