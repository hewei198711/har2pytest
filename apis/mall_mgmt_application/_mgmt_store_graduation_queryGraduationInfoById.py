import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_graduation_queryGraduationInfoById(params=params, headers=headers):
    """
    根据id查询结业申请详情
    /mgmt/store/graduation/queryGraduationInfoById

    参数说明:
    - id: id
    """

    url = "/mgmt/store/graduation/queryGraduationInfoById"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
