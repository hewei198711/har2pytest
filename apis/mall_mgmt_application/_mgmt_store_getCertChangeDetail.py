import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getCertChangeDetail(params=params, headers=headers):
    """
    获取电子印章信息变更详情
    /mgmt/store/getCertChangeDetail

    参数说明:
    - id: id
    """

    url = "/mgmt/store/getCertChangeDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
